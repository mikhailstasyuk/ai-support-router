import logging

from ..flows.escalation_flow import stt_repeat_then_handoff

logger = logging.getLogger(__name__)


class VoiceTurnLoop:
    def __init__(self, app, stt_adapter, metrics) -> None:
        self.app = app
        self.stt_adapter = stt_adapter
        self.metrics = metrics

    def run(self, caller_id: str = "caller-001") -> None:
        print("Voice loop started. Provide a .wav file path per turn ('exit' to stop).")
        stt_fail_streak = 0
        while True:
            wav_path = input("Caller (.wav path)> ").strip()
            if wav_path.lower() in {"exit", "quit"}:
                print("Voice loop ended.")
                break
            logger.info("caller_wav_path=%s", wav_path)

            ok, transcript = self.stt_adapter.transcribe_wav_file(wav_path)
            if not ok:
                self.metrics.stt_failures += 1
                stt_fail_streak += 1
                repeat = stt_repeat_then_handoff(stt_fail_streak)
                self.metrics.stt_deterministic_fallbacks += 1
                print("Assistant>", repeat["spoken_message"])
                reason = getattr(self.stt_adapter, "last_error", "")
                if reason:
                    print("Assistant> STT debug:", reason)
                if repeat.get("response_type") == "handoff":
                    self.metrics.handoffs += 1
                    stt_fail_streak = 0
                continue
            stt_fail_streak = 0
            logger.info("transcribed_text=%s", transcript)
            print(f"Assistant> Transcribed text: {transcript}")

            response = self.app.handle_turn(caller_id=caller_id, utterance=transcript)
            if response.get("response_type") == "handoff":
                self.metrics.handoffs += 1

            print("Assistant>", response.get("spoken_message", ""))
            logger.info("assistant_message=%s", response.get("spoken_message", ""))

            self.metrics.record_turn(success=response.get("response_type") != "handoff", playback_within_8s=True)
        score_raw = input("Assistant> Optional clarity feedback (1-5, Enter to skip): ").strip()
        if score_raw.isdigit():
            entry = self.app.capture_feedback(caller_id, "voice", int(score_raw))
            if entry:
                self.metrics.record_clarity_score(entry["clarity_score"])
