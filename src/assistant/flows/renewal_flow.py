def handle_renewal(payload: dict, repos) -> dict:
    renewal_id = payload.get("renewal_id", f"REN-{len(repos.renewals.all()) + 1:04d}")
    record = {
        "renewal_id": renewal_id,
        "policy_number": payload.get("policy_number"),
        "tariff_choice": payload.get("tariff_choice"),
        "selected_tariff_plan": payload.get("selected_tariff_plan"),
        "clinic_choice": payload.get("clinic_choice"),
        "selected_clinic": payload.get("selected_clinic"),
        "status": "submitted",
    }
    repos.renewals.save(renewal_id, record)
    return {"ok": True, "record": record, "message": f"Renewal request {renewal_id} submitted."}
