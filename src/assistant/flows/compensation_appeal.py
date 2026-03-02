def start_appeal(payload: dict, repos) -> dict:
    policy_id = payload.get("policy_id")
    reason = payload.get("appeal_reason")
    missing = []
    if not policy_id:
        missing.append("policy_id")
    if not reason:
        missing.append("appeal_reason")

    if missing:
        return {
            "ok": False,
            "missing_items": missing,
            "next_steps": "Please provide the missing items so I can submit the appeal.",
        }

    case_id = payload.get("case_id", f"CMP-{len(repos.compensations.all()) + 1:04d}")
    record = {
        "case_id": case_id,
        "policy_id": policy_id,
        "current_status": "under_review",
        "appeal_requested": True,
        "appeal_reason": reason,
        "missing_items": [],
        "next_steps": "Your appeal is submitted. Expect an update within 3 business days.",
    }
    repos.compensations.save(case_id, record)
    return {"ok": True, "record": record}
