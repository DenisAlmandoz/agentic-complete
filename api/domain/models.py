from __future__ import annotations

from enum import StrEnum
from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel, Field


class Language(StrEnum):
    ENGLISH = "english"
    SPANISH = "spanish"


class CefrLevel(StrEnum):
    A1 = "A1"
    A2 = "A2"
    B1 = "B1"
    B2 = "B2"
    C1 = "C1"
    C2 = "C2"


class AgentRole(StrEnum):
    COORDINATOR = "coordinator"
    PLANNER = "planner"
    TEACHER = "teacher"
    EXAMINER = "examiner"
    READINESS_ASSESSOR = "readiness_assessor"


class Topic(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    description: str
    specialized_prompt: str


class LearnerProfile(BaseModel):
    user_id: str
    native_language: Language | None = None
    target_language: Language = Language.ENGLISH
    current_level: CefrLevel = CefrLevel.A1
    goals: list[str] = Field(default_factory=list)


class ConversationTurn(BaseModel):
    speaker: Literal["learner", "agent"]
    text: str
    audio_url: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class TutorRequest(BaseModel):
    user_id: str
    target_language: Language
    topic: str
    message: str | None = None
    audio_base64: str | None = None
    requested_agent: AgentRole | None = None


class SkillScore(BaseModel):
    grammar: float = Field(ge=0, le=1)
    vocabulary: float = Field(ge=0, le=1)
    fluency: float = Field(ge=0, le=1)
    comprehension: float = Field(ge=0, le=1)
    pronunciation: float | None = Field(default=None, ge=0, le=1)

    @property
    def average(self) -> float:
        values = [self.grammar, self.vocabulary, self.fluency, self.comprehension]
        if self.pronunciation is not None:
            values.append(self.pronunciation)
        return sum(values) / len(values)


class LevelAssessment(BaseModel):
    current_level: CefrLevel
    recommended_level: CefrLevel
    can_promote: bool
    confidence: float = Field(ge=0, le=1)
    scores: SkillScore
    exam_required: bool = True
    rationale: str
    next_steps: list[str]


class TutorResponse(BaseModel):
    session_id: str
    agent_role: AgentRole
    reply: str
    assessment: LevelAssessment | None = None
    retrieved_context: list[str] = Field(default_factory=list)
    suggested_exercises: list[str] = Field(default_factory=list)
