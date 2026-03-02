from dataclasses import dataclass

try:
    import numpy as np
except Exception:  # pragma: no cover - optional local dependency
    np = None

try:
    import sounddevice as sd
except Exception:  # pragma: no cover - optional local dependency
    sd = None


@dataclass
class Chirp3AudioOutputAdapter:
    def play(self, voice_payload: dict) -> tuple[bool, str]:
        text = voice_payload.get("text", "")
        audio_bytes = voice_payload.get("audio_bytes")
        sample_rate_hz = int(voice_payload.get("sample_rate_hz", 16000))
        if audio_bytes and sd is not None and np is not None:
            try:
                pcm = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0
                sd.play(pcm, sample_rate_hz)
                sd.wait()
                return True, "played_audio_bytes"
            except Exception:
                pass
        if text:
            print(f"Assistant (voice): {text}")
            return True, "played_text_fallback"
        return False, "empty_audio"
