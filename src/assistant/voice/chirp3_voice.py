import os

try:
    from google.cloud import texttospeech
except Exception:  # pragma: no cover - optional provider dependency
    texttospeech = None


class Chirp3VoiceAdapter:
    def __init__(self) -> None:
        self.voice_name = os.getenv("CHIRP3_TTS_VOICE", "en-US-Chirp3-HD-Charon")
        self.language_code = os.getenv("CHIRP3_STT_LANGUAGE", "en-US")
        self.sample_rate_hz = int(os.getenv("AUDIO_SAMPLE_RATE", "16000"))
        self._client = texttospeech.TextToSpeechClient() if texttospeech is not None else None

    def synthesize(self, text: str) -> dict:
        if not text:
            return self.fallback_voice_message("empty_text")
        if self._client is None:
            return {
                "provider": "google_chirp3",
                "voice": self.voice_name,
                "text": text,
                "ok": True,
                "audio_bytes": b"",
                "sample_rate_hz": self.sample_rate_hz,
            }
        try:
            request = texttospeech.SynthesizeSpeechRequest(
                input=texttospeech.SynthesisInput(text=text),
                voice=texttospeech.VoiceSelectionParams(
                    language_code=self.language_code,
                    name=self.voice_name,
                ),
                audio_config=texttospeech.AudioConfig(
                    audio_encoding=texttospeech.AudioEncoding.LINEAR16,
                    sample_rate_hertz=self.sample_rate_hz,
                ),
            )
            response = self._client.synthesize_speech(request=request)
            return {
                "provider": "google_chirp3",
                "voice": self.voice_name,
                "text": text,
                "ok": True,
                "audio_bytes": response.audio_content,
                "sample_rate_hz": self.sample_rate_hz,
            }
        except Exception as exc:
            return self.fallback_voice_message(f"provider_error:{exc.__class__.__name__}")

    def fallback_voice_message(self, reason: str) -> dict:
        return {
            "provider": "fallback",
            "voice": "fallback-default",
            "text": "I can continue with a fallback voice right now, or connect you to a human agent.",
            "ok": False,
            "reason": reason,
            "audio_bytes": b"",
            "sample_rate_hz": self.sample_rate_hz,
        }
