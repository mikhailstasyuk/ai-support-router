from dataclasses import dataclass
from pathlib import Path
import os
import wave

try:
    from google.cloud import speech
except Exception:  # pragma: no cover - optional provider dependency
    speech = None


@dataclass
class Chirp3STTAdapter:
    language_code: str = "en-US"
    sample_rate_hz: int = 16000
    max_attempts: int = 2
    last_error: str = ""

    def transcribe(self, audio_bytes: bytes, typed_fallback: str | None = None, attempt: int = 1) -> tuple[bool, str]:
        if typed_fallback is not None:
            self.last_error = ""
            return True, typed_fallback
        if attempt > self.max_attempts:
            self.last_error = "stt_attempt_limit_exceeded"
            return False, ""
        if not audio_bytes:
            self.last_error = "empty_audio_content"
            return False, ""
        if speech is None:
            self.last_error = "google_cloud_speech_not_installed"
            return False, ""
        if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
            self.last_error = "google_application_credentials_missing"
            return False, ""
        try:
            client = speech.SpeechClient()
            audio = speech.RecognitionAudio(content=audio_bytes)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=self.sample_rate_hz,
                language_code=self.language_code,
            )
            response = client.recognize(config=config, audio=audio)
            transcripts = [res.alternatives[0].transcript for res in response.results if res.alternatives]
            merged = " ".join(t.strip() for t in transcripts if t.strip())
            if merged:
                self.last_error = ""
                return True, merged
            self.last_error = "no_transcript_returned"
            return False, ""
        except Exception as exc:
            self.last_error = f"google_stt_error:{exc.__class__.__name__}"
            return False, ""

    def transcribe_wav_file(self, wav_path: str, attempt: int = 1) -> tuple[bool, str]:
        if attempt > self.max_attempts:
            self.last_error = "stt_attempt_limit_exceeded"
            return False, ""
        path = Path(wav_path)
        if not path.exists() or not path.is_file():
            self.last_error = "wav_file_not_found"
            return False, ""
        try:
            with wave.open(str(path), "rb") as wf:
                channels = wf.getnchannels()
                sample_width = wf.getsampwidth()
                sample_rate = wf.getframerate()
                frames = wf.readframes(wf.getnframes())
            if channels != 1 or sample_width != 2 or not frames:
                self.last_error = (
                    f"unsupported_wav_format:channels={channels},sample_width={sample_width},frames={len(frames)}"
                )
                return False, ""
            self.sample_rate_hz = sample_rate
            return self.transcribe(frames, typed_fallback=None, attempt=attempt)
        except Exception as exc:
            self.last_error = f"wav_read_error:{exc.__class__.__name__}"
            return False, ""
