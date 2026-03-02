from .constants import Intent
from .flows.appointment_flow import handle_appointment
from .flows.callback_flow import handle_callback
from .flows.clinic_flow import check_clinic_eligibility
from .flows.compensation_appeal import start_appeal
from .flows.compensation_flow import check_status
from .flows.renewal_flow import handle_renewal
from .flows.plan_flow import summarize_plans
from .guards import is_verified, requires_verification
from .prompting.appointment_prompts import appointment_candidate_prompt, appointment_confirmation
from .prompting.policy_prompts import clinic_alternatives, plan_summary_response, renewal_confirmation


class Router:
    def __init__(self, store, fallback_factory):
        self.store = store
        self.fallback_factory = fallback_factory

    def reject_payment(self, utterance: str) -> dict | None:
        if "payment" in utterance.lower():
            return {
                "response_type": "next_steps",
                "spoken_message": "Payment processing is not available in this prototype. I can transfer you to a human billing agent.",
                "next_expected_input": "Say transfer for billing",
                "collected_fields_delta": {},
            }
        return None

    def dispatch(self, intent: Intent, payload: dict, caller_profile: dict) -> dict:
        if requires_verification(intent) and not is_verified(caller_profile):
            return {
                "response_type": "next_steps",
                "spoken_message": "Please complete identity verification before this action.",
                "next_expected_input": "Provide verification code",
                "collected_fields_delta": {},
            }

        repos = self.store.repos
        if intent in {Intent.SCHEDULE_APPOINTMENT, Intent.UPDATE_APPOINTMENT, Intent.CANCEL_APPOINTMENT, Intent.REBOOK_APPOINTMENT}:
            operation_map = {
                Intent.SCHEDULE_APPOINTMENT: "book",
                Intent.UPDATE_APPOINTMENT: "update",
                Intent.CANCEL_APPOINTMENT: "cancel",
                Intent.REBOOK_APPOINTMENT: "rebook",
            }
            payload.setdefault("operation", operation_map[intent])
            result = handle_appointment(payload, repos)
            if result.get("needs_selection"):
                return {
                    "response_type": "alternative_offer",
                    "spoken_message": appointment_candidate_prompt(result.get("matches", [])),
                    "payload": result,
                    "collected_fields_delta": {},
                    "next_expected_input": "Choose appointment candidate",
                }
            spoken = appointment_confirmation(result.get("record", {}).get("appointment_id", ""))
            return {"response_type": "success", "spoken_message": spoken, "payload": result, "collected_fields_delta": {}, "next_expected_input": "Anything else?"}
        if intent == Intent.RENEW_POLICY:
            result = handle_renewal(payload, repos)
            return {"response_type": "success", "spoken_message": renewal_confirmation(result["record"]["renewal_id"]), "payload": result, "collected_fields_delta": {}, "next_expected_input": "Anything else?"}
        if intent == Intent.INQUIRE_PLANS:
            summary = summarize_plans(payload, repos.plans.all())
            return {"response_type": "success", "spoken_message": plan_summary_response(summary), "collected_fields_delta": {}, "next_expected_input": "Would you like to choose one?"}
        if intent == Intent.CHANGE_CLINIC:
            result = check_clinic_eligibility(payload, repos.policies.all())
            if result["eligibility_result"] != "eligible":
                return {
                    "response_type": "alternative_offer",
                    "spoken_message": clinic_alternatives(payload.get("clinic_name") or payload.get("requested_clinic") or "requested clinic", result["alternatives"]),
                    "collected_fields_delta": {},
                    "next_expected_input": "Choose one alternative",
                }
            return {"response_type": "success", "spoken_message": "Clinic change is eligible and recorded.", "collected_fields_delta": {}, "next_expected_input": "Anything else?"}
        if intent == Intent.REQUEST_CALLBACK:
            result = handle_callback(payload, repos)
            return {"response_type": "success", "spoken_message": result["message"], "payload": result, "collected_fields_delta": {}, "next_expected_input": "Anything else?"}
        if intent == Intent.CHECK_COMPENSATION_STATUS:
            result = check_status(payload, repos)
            return {
                "response_type": "success" if result.get("ok") else "next_steps",
                "spoken_message": result.get("status") or result.get("message"),
                "next_expected_input": result.get("next_steps", "Anything else?"),
                "collected_fields_delta": {},
            }
        if intent == Intent.SUBMIT_COMPENSATION_APPEAL:
            result = start_appeal(payload, repos)
            if not result.get("ok"):
                msg = f"Missing: {', '.join(result['missing_items'])}. {result['next_steps']}"
                return {"response_type": "next_steps", "spoken_message": msg, "next_expected_input": "Provide missing items", "collected_fields_delta": {}}
            return {"response_type": "success", "spoken_message": "Compensation appeal submitted.", "payload": result, "next_expected_input": "Anything else?", "collected_fields_delta": {}}

        return self.fallback_factory.llm_unavailable_fallback()
