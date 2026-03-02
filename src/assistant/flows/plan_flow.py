def summarize_plans(payload: dict, plans: list[dict]) -> str:
    if payload.get("all_plans"):
        selected = plans
    elif payload.get("plan_name"):
        selected = [p for p in plans if payload["plan_name"].lower() in p.get("name", "").lower()]
    elif payload.get("cost_range"):
        selected = [p for p in plans if payload["cost_range"] in p.get("cost_band", "")]
    else:
        selected = plans[:3]

    if not selected:
        return "I could not find matching plans. I can connect you to an agent for a tailored recommendation."
    top = selected[:3]
    parts = [f"{p['name']} ({p.get('cost_band', 'n/a')})" for p in top]
    return "Top options: " + ", ".join(parts)
