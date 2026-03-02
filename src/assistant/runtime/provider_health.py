from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ProviderStatus:
    openai_available: bool = True
    chirp3_stt_available: bool = True
    chirp3_tts_available: bool = True


class ProviderHealthChecker:
    def evaluate(self, openai_client: object | None, voice_adapter: object | None) -> ProviderStatus:
        return ProviderStatus(
            openai_available=openai_client is not None,
            chirp3_stt_available=voice_adapter is not None,
            chirp3_tts_available=voice_adapter is not None,
        )

