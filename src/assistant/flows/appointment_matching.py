def find_recent_matches(appointments: list[dict], policy_id: str, operation: str) -> list[dict]:
    candidates = [a for a in appointments if a.get("policy_id") == policy_id and a.get("status") == "confirmed"]
    if operation == "cancel":
        return candidates[:5]
    return sorted(candidates, key=lambda x: x.get("date", ""), reverse=True)[:5]
