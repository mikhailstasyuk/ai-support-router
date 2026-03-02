def check_clinic_eligibility(payload: dict, policies: list[dict], clinics: list[str] | None = None) -> dict:
    requested = payload.get("clinic_name") or payload.get("requested_clinic")
    clinics = clinics or ["Downtown Clinic", "North Care Center", "Metro Health Hub"]
    if requested in clinics:
        return {"eligibility_result": "eligible", "alternatives": []}
    return {
        "eligibility_result": "ineligible",
        "alternatives": clinics[:2],
    }
