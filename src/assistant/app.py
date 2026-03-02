from __future__ import annotations

import argparse
from datetime import datetime, UTC

from .config import AppConfig, configure_logging
from .constants import Intent
from .flows.escalation_flow import escalate_to_human
from .flows.fallback_flow import llm_unavailable_fallback, tts_unavailable_fallback
from .flows.intake_flow import run_intake
from .flows.verification_flow import register_failure_and_check, verify
from .guards import requires_verification
from .handoff import pack_verification_failure_handoff
from .llm.openai_agent import OpenAIAgent
from .metrics import Metrics
from .prompting.next_step_prompts import missing_info_prompt
from .prompting.verification_prompts import build_verification_prompt
from .router import Router
from .store.store import AssistantStore
from .validation import enforce_next_step_limit, normalize_response, validate_intent_payload
from .voice.stt_adapter import Chirp3STTAdapter
from .runtime.session_state import ConversationSessionState
from .runtime.text_turn_loop import TextTurnLoop
from .runtime.turn_manager import TurnManager
from .runtime.voice_turn_loop import VoiceTurnLoop


class FallbackFactory:
    llm_unavailable_fallback = staticmethod(llm_unavailable_fallback)
    tts_unavailable_fallback = staticmethod(tts_unavailable_fallback)


class AssistantApp:
    def __init__(self) -> None:
        self.config = AppConfig()
        self.store = AssistantStore(self.config.data_dir)
        self.agent = OpenAIAgent(self.config.openai_model)
        self.router = Router(self.store, FallbackFactory)
        self.sessions: dict[str, ConversationSessionState] = {}
        self.turn_manager = TurnManager()

    def _ensure_caller(self, caller_id: str) -> dict:
        caller = self.store.repos.callers.get(caller_id)
        if caller:
            return caller
        caller = {
            "caller_id": caller_id,
            "caller_type": "policy_holder",
            "phone_number": "+10000000000",
            "verification_state": "pending",
        }
        self.store.repos.callers.save(caller_id, caller)
        return caller

    def _session(self, caller_id: str) -> ConversationSessionState:
        return self.sessions.setdefault(caller_id, ConversationSessionState(caller_id=caller_id))

    def capture_feedback(self, caller_id: str, mode: str, clarity_score: int | None) -> dict | None:
        if clarity_score is None or clarity_score < 1 or clarity_score > 5:
            return None
        feedback_id = f"FDB-{len(self.store.repos.feedback.all()) + 1:04d}"
        entry = {
            "feedback_id": feedback_id,
            "caller_id": caller_id,
            "mode": mode,
            "clarity_score": clarity_score,
            "captured_at": datetime.now(UTC).isoformat(),
        }
        self.store.repos.feedback.save(feedback_id, entry)
        return entry

    def handle_turn(self, caller_id: str, utterance: str, payload: dict | None = None) -> dict:
        payload = payload or {}
        self.store.begin_turn(caller_id)
        session = self._session(caller_id)
        session.begin_turn()
        payment_block = self.router.reject_payment(utterance)
        if payment_block:
            return normalize_response(payment_block)

        caller = self._ensure_caller(caller_id)
        intent = self.turn_manager.infer_intent(session)
        if intent is None:
            intake = run_intake(utterance, self.agent, self.store, caller_id)
            intent = intake["intent"]
            if intent == Intent.HANDOFF_TO_HUMAN:
                session.clear_pending()
                return normalize_response(escalate_to_human(
                    intent="unknown",
                    caller_type=caller.get("caller_type", "unknown"),
                    collected_fields=payload,
                    retry_count=intake.get("retry_count", 0),
                    blocker_reason="intent_unresolved",
                ))
            if intent == Intent.UNKNOWN:
                return normalize_response({
                    "response_type": "clarification",
                    "spoken_message": intake["spoken_message"],
                    "next_expected_input": "Clarify request",
                    "collected_fields_delta": {},
                })
            session.pending_intent = intent
        payload = self.turn_manager.extract_from_utterance(intent, utterance, payload | session.collected_payload)
        session.collected_payload = dict(payload)

        if requires_verification(intent):
            if "verification_code" not in payload:
                session.awaiting_verification = True
                session.pending_intent = intent
                return normalize_response({
                    "response_type": "next_steps",
                    "spoken_message": build_verification_prompt(caller_id),
                    "next_expected_input": "Provide verification code",
                    "collected_fields_delta": {},
                })
            is_ok, state = verify(caller, payload.get("verification_code"))
            self.store.repos.callers.save(caller_id, caller)
            if not is_ok:
                failures, should_handoff = register_failure_and_check(self.store, caller_id)
                if should_handoff:
                    summary = pack_verification_failure_handoff(
                        {
                            "intent": intent.value,
                            "caller_type": caller.get("caller_type", "unknown"),
                            "verification_state": state,
                            "verification_attempts": failures,
                            "provided_fields": list(payload.keys()),
                        },
                        failures,
                    )
                    return normalize_response({
                        "response_type": "handoff",
                        "spoken_message": "I cannot verify identity in this call. I will transfer you to a human agent.",
                        "next_expected_input": "Please wait for transfer",
                        "collected_fields_delta": {},
                        "handoff_summary": summary.__dict__,
                    })
                session.awaiting_verification = True
                session.pending_intent = intent
                return normalize_response({
                    "response_type": "clarification",
                    "spoken_message": "Verification failed. Please provide the code again.",
                    "next_expected_input": "Provide verification code",
                    "collected_fields_delta": {},
                })
            session.awaiting_verification = False

        missing = validate_intent_payload(intent, payload)
        if missing:
            session.set_pending(intent, missing)
            return normalize_response({
                "response_type": "next_steps",
                "spoken_message": enforce_next_step_limit(missing_info_prompt(intent.value, missing)),
                "next_expected_input": "Provide missing details",
                "collected_fields_delta": {},
                "missing_fields": missing,
            })

        session.clear_pending()
        return normalize_response(self.router.dispatch(intent, payload, caller))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--voice-loop", action="store_true", help="Run .wav-to-text loop mode")
    args = parser.parse_args()

    app = AssistantApp()
    configure_logging(app.config.log_level)
    if args.voice_loop:
        metrics = Metrics()
        stt_adapter = Chirp3STTAdapter(
            language_code=app.config.chirp3_stt_language,
            sample_rate_hz=app.config.audio_sample_rate,
        )
        loop = VoiceTurnLoop(app, stt_adapter, metrics)
        loop.run()
        print("Metrics:", metrics.to_summary())
    else:
        TextTurnLoop(app).run()


if __name__ == "__main__":
    main()
