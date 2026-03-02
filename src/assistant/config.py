from dataclasses import dataclass
import logging
import os


@dataclass
class AppConfig:
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    data_dir: str = os.getenv("DATA_DIR", "data/mock")
    chirp3_voice: str = os.getenv("CHIRP3_TTS_VOICE", "en-US-Chirp3-HD-Charon")
    chirp3_stt_language: str = os.getenv("CHIRP3_STT_LANGUAGE", "en-US")
    audio_sample_rate: int = int(os.getenv("AUDIO_SAMPLE_RATE", "16000"))
    audio_channels: int = int(os.getenv("AUDIO_CHANNELS", "1"))
    runtime_mode: str = os.getenv("RUNTIME_MODE", "text")
    deterministic_fallbacks: bool = os.getenv("DETERMINISTIC_FALLBACKS", "true").lower() == "true"
    log_level: str = os.getenv("LOG_LEVEL", "INFO")


def configure_logging(level: str = "INFO") -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
