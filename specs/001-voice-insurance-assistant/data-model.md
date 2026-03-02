# Data Model: Voice-First Insurance Assistant

## 1. CallerProfile

### Fields
- `caller_id` (string, required)
- `caller_type` (enum, required): `policy_holder`, `prospective_customer`
- `phone_number` (string, optional)
- `verification_state` (enum, required): `not_required`, `pending`, `verified`, `failed`, `escalated`
- `active_intent` (enum, optional)

### Validation Rules
- `caller_type` must be known before sensitive actions.
- `verification_state=verified` is required for sensitive policy-holder operations.

### Relationships
- One caller can initiate multiple intent flows in a single session.

## 2. PolicyRecord

### Fields
- `policy_id` (string, optional)
- `policy_number` (string, optional)
- `tariff_plan` (string, optional)
- `clinic` (string, optional)
- `eligibility_state` (enum, optional): `eligible`, `ineligible`, `unknown`

### Validation Rules
- At least one policy identifier is required for protected policy operations.
- Sensitive actions require verified caller state.

### Relationships
- One policy can have many appointments and compensation cases.

## 3. AppointmentRequest

### Fields
- `operation` (enum, required): `book`, `update`, `cancel`, `rebook`
- `policy_id` (string, required for protected operations)
- `preferred_date` (date, optional)
- `doctor_name` (string, optional)
- `doctor_specialization` (string, optional)
- `clinic` (string, optional)
- `appointment_id` (string, optional)
- `candidate_matches` (list, optional)
- `status` (enum, required): `initiated`, `matched`, `confirmed`, `cancelled`, `failed`, `escalated`

### Validation Rules
- `book` requires `policy_id`, `preferred_date`, `clinic`, and one of doctor name/specialization.
- `update` and `cancel` require appointment ID or candidate selection.
- Unavailable slots must return alternatives when available.

### State Transitions
- `initiated -> matched -> confirmed`
- `initiated -> failed -> escalated`
- `confirmed -> cancelled`

## 4. RenewalRequest

### Fields
- `renewal_id` (string, required)
- `policy_number` (string, required)
- `tariff_choice` (enum, required): `same`, `new`
- `selected_tariff_plan` (string, optional)
- `clinic_choice` (enum, required): `same`, `new`
- `selected_clinic` (string, optional)
- `status` (enum, required): `initiated`, `submitted`, `needs_followup`, `escalated`

### Validation Rules
- `policy_number` is mandatory.
- If `tariff_choice=new`, selected tariff must be provided.
- If `clinic_choice=new`, selected clinic must be provided.

## 5. PlanInquiry

### Fields
- `inquiry_type` (enum, required): `plan_name`, `cost_range`, `all_plans`
- `plan_name_filter` (string, optional)
- `cost_range_filter` (string, optional)
- `comparison_summary` (string, required once answered)
- `status` (enum, required): `initiated`, `answered`, `escalated`

### Validation Rules
- At least one filter is required unless inquiry is `all_plans`.
- Returned summary must be concise and decision-oriented.

## 6. ClinicChangeRequest

### Fields
- `request_mode` (enum, required): `clinic_name`, `location`, `nearby_metro`
- `requested_clinic` (string, optional)
- `requested_location` (string, optional)
- `requested_metro` (string, optional)
- `eligibility_result` (enum, required): `eligible`, `ineligible`, `unavailable`, `unknown`
- `alternatives` (list, optional)
- `status` (enum, required): `initiated`, `resolved`, `needs_alternative`, `escalated`

### Validation Rules
- One request mode and corresponding value must be present.
- Ineligible/unavailable outcomes must include alternatives when available.

## 7. CallbackRequest

### Fields
- `callback_id` (string, required)
- `topic` (string, required)
- `phone_number` (string, required)
- `preferred_window` (string, required)
- `policy_id` (string, optional)
- `status` (enum, required): `captured`, `queued`, `failed`

### Validation Rules
- Callback must be accepted without policy ID.
- Topic, phone number, and preferred window are always required.

## 8. CompensationCase

### Fields
- `case_id` (string, required)
- `policy_id` (string, required)
- `current_status` (string, required)
- `appeal_requested` (boolean, required)
- `appeal_reason` (string, conditionally required)
- `missing_items` (list, optional)
- `next_steps` (string, required when incomplete)

### Validation Rules
- Status checks require verified caller and policy ID.
- Appeal requires policy ID plus appeal reason.
- Missing items require explicit next-step guidance.

### State Transitions
- `status_checked -> complete`
- `status_checked -> incomplete -> awaiting_documents`
- `status_checked -> appeal_initiated -> under_review`

## 9. HandoffSummary

### Fields
- `intent` (string, required)
- `caller_type` (string, required)
- `verification_outcome` (string, required)
- `collected_fields` (map, required)
- `retry_count` (integer, required)
- `blocker_reason` (string, required)
- `recommended_next_action` (string, required)

### Validation Rules
- Handoff summary is required for every automated transfer.
- Collected fields must include caller-provided details from the active flow.

## 10. CallerFeedback

### Fields
- `feedback_id` (string, required)
- `caller_id` (string, required)
- `mode` (enum, required): `text`, `voice`
- `clarity_score` (integer, optional): `1..5`
- `comment` (string, optional)
- `captured_at` (string timestamp, required)

### Validation Rules
- `clarity_score` is optional, but when present must be within 1 to 5.
- Feedback capture must not block flow completion or handoff.

### Relationships
- Belongs to one caller session and is aggregated in metrics reporting.
