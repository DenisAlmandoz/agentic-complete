from __future__ import annotations

from abc import ABC, abstractmethod

from api.domain.models import AgentRole, TutorRequest, TutorResponse


class Agent(ABC):
    role: AgentRole

    @abstractmethod
    def run(self, request: TutorRequest, context: list[str]) -> TutorResponse:
        raise NotImplementedError
