from __future__ import annotations


import logging

logger = logging.getLogger(__name__)


class TextTurnLoop:
    def __init__(self, app) -> None:
        self.app = app

    def run(self) -> None:
        print("Assistant started in text mode. Type 'exit' to stop.")
        caller_id = input("Caller ID [caller-001]> ").strip() or "caller-001"
        while True:
            utterance = input("Caller> ").strip()
            if utterance.lower() in {"exit", "quit"}:
                break
            logger.info("caller_text=%s", utterance)
            response = self.app.handle_turn(caller_id, utterance)
            print("Assistant>", response.get("spoken_message"))
            logger.info("assistant_message=%s", response.get("spoken_message"))
        score_raw = input("Assistant> Optional clarity feedback (1-5, Enter to skip): ").strip()
        if score_raw.isdigit():
            self.app.capture_feedback(caller_id, "text", int(score_raw))
