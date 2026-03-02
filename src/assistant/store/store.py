from dataclasses import dataclass

from .file_backend import FileBackend
from .repositories import Repositories


@dataclass
class TurnState:
    caller_id: str
    turn_index: int = 0
    clarification_retries: int = 0
    verification_failures: int = 0


class AssistantStore:
    def __init__(self, base_dir: str = "data/mock") -> None:
        self.backend = FileBackend(base_dir)
        self.repos = Repositories(self.backend)
        self.turn_state: dict[str, TurnState] = {}

    def begin_turn(self, caller_id: str) -> TurnState:
        # Force fresh file reads each turn by recreating repositories.
        self.repos = Repositories(self.backend)
        state = self.turn_state.setdefault(caller_id, TurnState(caller_id=caller_id))
        state.turn_index += 1
        return state

    def reset_clarification(self, caller_id: str) -> None:
        self.turn_state.setdefault(caller_id, TurnState(caller_id=caller_id)).clarification_retries = 0

    def increment_clarification(self, caller_id: str) -> int:
        state = self.turn_state.setdefault(caller_id, TurnState(caller_id=caller_id))
        state.clarification_retries += 1
        return state.clarification_retries

    def increment_verification_failure(self, caller_id: str) -> int:
        state = self.turn_state.setdefault(caller_id, TurnState(caller_id=caller_id))
        state.verification_failures += 1
        return state.verification_failures
