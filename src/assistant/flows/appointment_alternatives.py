def offer_alternatives(plans: list[dict], clinic: str, preferred_date: str) -> list[str]:
    # Prototype deterministic alternatives.
    return [
        f"{clinic} on {preferred_date} at 11:00",
        f"{clinic} on {preferred_date} at 15:00",
        f"{clinic} next business day at 10:30",
    ]
