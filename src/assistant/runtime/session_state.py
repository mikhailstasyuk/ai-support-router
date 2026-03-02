from __future__ import annotations

from dataclasses import dataclass, field

from ..constants import Intent


@dataclass
class ConversationSessionState:
    caller_id: str
    pending_intent: Intent | None = None
    awaiting_verification: bool = False
    missing_fields: list[str] = field(default_factory=list)
    collected_payload: dict = field(default_factory=dict)
    turn_index: int = 0

    def begin_turn(self) -> None:
        self.turn_index += 1

    def set_pending(self, intent: Intent, missing_fields: list[str]) -> None:
        self.pending_intent = intent
        self.missing_fields = list(missing_fields)

    def clear_pending(self) -> None:
        self.pending_intent = None
        self.awaiting_verification = False
        self.missing_fields = []
        self.collected_payload = {}

