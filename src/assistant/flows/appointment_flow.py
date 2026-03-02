from .appointment_matching import find_recent_matches
from .appointment_alternatives import offer_alternatives


def handle_appointment(payload: dict, repos) -> dict:
    operation = payload.get("operation", "book")
    if operation == "book":
        appt_id = payload.get("appointment_id", f"APT-{len(repos.appointments.all()) + 1:04d}")
        record = {
            "appointment_id": appt_id,
            "policy_id": payload.get("policy_id"),
            "date": payload.get("preferred_date"),
            "doctor": payload.get("doctor_name") or payload.get("doctor_specialization"),
            "clinic": payload.get("clinic"),
            "status": "confirmed",
        }
        repos.appointments.save(appt_id, record)
        return {"ok": True, "message": f"Appointment {appt_id} confirmed.", "record": record}

    if operation in {"update", "cancel"}:
        appt_id = payload.get("appointment_id")
        if not appt_id:
            matches = find_recent_matches(repos.appointments.all(), payload.get("policy_id", ""), operation)
            return {"ok": False, "needs_selection": True, "matches": matches}
        status = "cancelled" if operation == "cancel" else "confirmed"
        updated = repos.appointments.save(appt_id, {"status": status, "date": payload.get("preferred_date")})
        return {"ok": True, "message": f"Appointment {appt_id} {status}.", "record": updated}

    if operation == "rebook":
        alternatives = offer_alternatives([], payload.get("clinic", "your clinic"), payload.get("preferred_date", "soon"))
        return {"ok": True, "alternatives": alternatives, "message": "Here are the earliest available slots."}

    return {"ok": False, "message": "Unsupported appointment operation."}
