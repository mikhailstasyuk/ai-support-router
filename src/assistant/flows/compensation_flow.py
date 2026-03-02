def check_status(payload: dict, repos) -> dict:
    policy_id = payload.get("policy_id")
    matches = repos.compensations.find(lambda c: c.get("policy_id") == policy_id)
    if not matches:
        return {
            "ok": False,
            "message": "No compensation case found for this policy ID.",
            "next_steps": "Share your case reference or speak to a human agent.",
        }
    case = matches[0]
    return {
        "ok": True,
        "status": case.get("current_status", "unknown"),
        "next_steps": case.get("next_steps", "We will notify you on the registered phone number."),
    }
