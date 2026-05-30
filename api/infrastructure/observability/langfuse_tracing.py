from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

from loguru import logger

from api.application.settings import Settings


class LangfuseTracer:
    def __init__(self, settings: Settings) -> None:
        self.enabled = bool(settings.langfuse_public_key and settings.langfuse_secret_key)
        self.settings = settings

    @contextmanager
    def trace(self, name: str, **metadata: object) -> Iterator[None]:
        if self.enabled:
            logger.info("Langfuse trace start: {name} {metadata}", name=name, metadata=metadata)
        try:
            yield
        finally:
            if self.enabled:
                logger.info("Langfuse trace end: {name}", name=name)
