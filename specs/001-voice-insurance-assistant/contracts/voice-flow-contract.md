# Voice Flow Contract

## 1. Input Envelope

- `utterance_text`: caller natural-language text/transcript
- `caller_context`: known profile/session attributes
- `turn_index`: current turn index
- `interaction_mode`: `voice` or `text`
- `audio_input_source`: `microphone` or configured call-audio source

## 2. Provider Contracts

- Primary agent LLM provider: OpenAI API
- Speech provider: Google Chirp-3 STT and Google Chirp-3 HD TTS

## 3. Supported Intents

- `schedule_appointment`
- `update_appointment`
- `cancel_appointment`
- `rebook_appointment`
- `renew_policy`
- `inquire_plans`
- `change_clinic`
- `request_callback`
- `check_compensation_status`
- `submit_compensation_appeal`
- `handoff_to_human`

## 4. Intent Resolution Rules

- Clear confidence -> immediate route.
- Ambiguous intent -> short clarification question.
- Two unresolved clarification attempts -> mandatory handoff.

## 5. Required Field Matrix

- `schedule_appointment`: `policy_id`, `preferred_date`, `clinic`, and doctor name or specialization
- `update_appointment` / `cancel_appointment`: `appointment_id` or selected candidate
- `rebook_appointment`: prior appointment reference or selected prior visit
- `renew_policy`: `policy_number`, `tariff_choice`, `clinic_choice`
- `inquire_plans`: one of `plan_name`, `cost_range`, `all_plans`
- `change_clinic`: one of `clinic_name`, `location`, `nearby_metro`
- `request_callback`: `topic`, `phone_number`, `preferred_callback_window` (`policy_id` optional)
- `check_compensation_status`: `policy_id`
- `submit_compensation_appeal`: `policy_id`, `appeal_reason`

## 6. Verification and Escalation

- Sensitive intents require verified identity.
- Three verification failures -> mandatory handoff.
- If live handoff is unavailable, assistant must provide alternate next steps and callback offer in the same interaction.

## 7. Response Schema

Each response includes:
- `response_type`: `success`, `clarification`, `alternative_offer`, `next_steps`, or `handoff`
- `spoken_message`
- `collected_fields_delta`
- `next_expected_input`

## 8. Handoff Summary Schema

Required fields:
- detected intent
- caller type
- verification outcome
- collected key fields
- retry count/failure reason
- unresolved blocker
- recommended next action

## 8A. Feedback Capture Schema

Optional end-of-interaction feedback includes:
- `clarity_score` (1..5)
- `mode` (`text` or `voice`)
- `captured_at`

## 9. Local Voice Loop Contract

For each turn:
- audio capture -> STT -> intent/flow handling -> TTS playback

Fallback rules:
- STT failure: one repeat prompt, then handoff offer.
- TTS failure: deterministic fallback message preserving business outcome.

## 10. Out of Scope

- Payment processing
- Production deployment/hardening
