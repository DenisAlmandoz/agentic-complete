from __future__ import annotations

import base64
import tempfile
from pathlib import Path

from loguru import logger


class WhisperTranscriber:
    """Whisper-compatible transcription boundary.

    Install an implementation such as `openai-whisper` or replace this adapter with a hosted speech API.
    """

    def __init__(self, model_name: str) -> None:
        self.model_name = model_name

    def transcribe_base64(self, audio_base64: str) -> str:
        audio_bytes = base64.b64decode(audio_base64)
        with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as file:
            file.write(audio_bytes)
            path = Path(file.name)
        logger.info("Received audio for Whisper transcription: {path}", path=path)
        return "[transcription pending: connect WhisperTranscriber to your chosen Whisper runtime]"
