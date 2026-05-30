from __future__ import annotations

from collections.abc import Sequence

from loguru import logger
from openai import OpenAI

from api.application.settings import Settings


class GrokClient:
    """Small xAI/Grok adapter using the OpenAI-compatible API surface."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.client = OpenAI(api_key=settings.xai_api_key, base_url=settings.xai_base_url)

    def chat(self, messages: Sequence[dict[str, str]], *, temperature: float = 0.4) -> str:
        logger.debug("Calling Grok model {model}", model=self.settings.grok_model)
        response = self.client.chat.completions.create(
            model=self.settings.grok_model,
            messages=list(messages),
            temperature=temperature,
        )
        return response.choices[0].message.content or ""
