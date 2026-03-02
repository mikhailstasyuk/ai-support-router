#!/usr/bin/env python3
import json
from pathlib import Path

SEED = {
    "callers": [
        {
            "caller_id": "caller-001",
            "caller_type": "policy_holder",
            "phone_number": "+15555550100",
            "verification_state": "pending",
        }
    ],
    "policies": [
        {
            "policy_id": "POL-1001",
            "policy_number": "PN-2026-1001",
            "tariff_plan": "Standard Care",
            "clinic": "Downtown Clinic",
            "eligibility_state": "eligible",
        }
    ],
    "plans": [
        {"plan_id": "PLN-1", "name": "Basic Shield", "cost_band": "low"},
        {"plan_id": "PLN-2", "name": "Standard Care", "cost_band": "medium"},
        {"plan_id": "PLN-3", "name": "Premium Plus", "cost_band": "high"},
    ],
    "appointments": [
        {
            "appointment_id": "APT-0001",
            "policy_id": "POL-1001",
            "date": "2026-03-10",
            "doctor": "Dr. Kim",
            "clinic": "Downtown Clinic",
            "status": "confirmed",
        }
    ],
    "renewals": [],
    "callbacks": [],
    "compensations": [
        {
            "case_id": "CMP-0001",
            "policy_id": "POL-1001",
            "current_status": "documents_review",
            "appeal_requested": False,
            "missing_items": ["medical_invoice"],
            "next_steps": "Upload the medical invoice to continue processing.",
        }
    ],
    "feedback": [],
}


def main() -> None:
    base = Path("data/mock")
    base.mkdir(parents=True, exist_ok=True)
    for domain, payload in SEED.items():
        with (base / f"{domain}.json").open("w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2)
    print("Mock data seeded")


if __name__ == "__main__":
    main()
