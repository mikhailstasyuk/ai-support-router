def handle_callback(payload: dict, repos) -> dict:
    callback_id = payload.get("callback_id", f"CB-{len(repos.callbacks.all()) + 1:04d}")
    record = {
        "callback_id": callback_id,
        "topic": payload.get("topic"),
        "phone_number": payload.get("phone_number"),
        "preferred_window": payload.get("preferred_callback_window"),
        "policy_id": payload.get("policy_id"),
        "status": "queued",
    }
    repos.callbacks.save(callback_id, record)
    return {"ok": True, "record": record, "message": f"Callback request {callback_id} queued."}
