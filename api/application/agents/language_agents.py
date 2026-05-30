from __future__ import annotations

from uuid import uuid4

from api.application.agents.base import Agent
from api.domain.models import AgentRole, CefrLevel, SkillScore, TutorRequest, TutorResponse
from api.domain.rubrics import CEFR_RUBRICS, decide_promotion
from api.infrastructure.llm.grok_client import GrokClient


class CoordinatorAgent(Agent):
    role = AgentRole.COORDINATOR

    def select_role(self, request: TutorRequest) -> AgentRole:
        message = (request.message or "").lower()
        if request.requested_agent:
            return request.requested_agent
        if "exam" in message or "test me" in message:
            return AgentRole.EXAMINER
        if "ready" in message or "level" in message or "a2" in message:
            return AgentRole.READINESS_ASSESSOR
        return AgentRole.TEACHER

    def run(self, request: TutorRequest, context: list[str]) -> TutorResponse:
        role = self.select_role(request)
        return TutorResponse(session_id=str(uuid4()), agent_role=self.role, reply=f"Coordinator selected {role.value}.")


class PlannerAgent(Agent):
    role = AgentRole.PLANNER

    def plan(self, request: TutorRequest, context: list[str]) -> list[str]:
        return [
            f"Warm up in {request.target_language} about {request.topic}.",
            "Ask one comprehension question.",
            "Correct only the two most important mistakes.",
            "End with an exam-readiness micro-assessment.",
        ]

    def run(self, request: TutorRequest, context: list[str]) -> TutorResponse:
        return TutorResponse(session_id=str(uuid4()), agent_role=self.role, reply="\n".join(self.plan(request, context)))


class TeacherAgent(Agent):
    role = AgentRole.TEACHER

    def __init__(self, llm: GrokClient) -> None:
        self.llm = llm

    def run(self, request: TutorRequest, context: list[str]) -> TutorResponse:
        system = (
            "You are a warm but rigorous CEFR language tutor. Teach only the target language unless a brief "
            "native-language clarification is necessary. Use retrieved context, adapt to the learner, and ask "
            "one next question."
        )
        prompt = f"Target language: {request.target_language}. Topic: {request.topic}. Context: {context}. Learner: {request.message}"
        reply = self.llm.chat([{"role": "system", "content": system}, {"role": "user", "content": prompt}])
        return TutorResponse(
            session_id=str(uuid4()),
            agent_role=self.role,
            reply=reply,
            retrieved_context=context,
            suggested_exercises=["Record a 60-second answer", "Write five sentences using today's corrections"],
        )


class ExaminerAgent(Agent):
    role = AgentRole.EXAMINER

    def run(self, request: TutorRequest, context: list[str]) -> TutorResponse:
        return TutorResponse(
            session_id=str(uuid4()),
            agent_role=self.role,
            reply=(
                f"Mini exam for {request.target_language} / {request.topic}: answer without notes. "
                "1) Summarize your opinion. 2) Ask me a follow-up question. 3) Correct your answer once."
            ),
        )


class ReadinessAssessorAgent(Agent):
    role = AgentRole.READINESS_ASSESSOR

    def run(self, request: TutorRequest, context: list[str]) -> TutorResponse:
        text = request.message or ""
        length_score = min(len(text.split()) / 80, 1.0)
        has_connectors = any(word in text.lower() for word in ["because", "although", "pero", "porque", "sin embargo"])
        scores = SkillScore(
            grammar=0.65 + 0.2 * length_score,
            vocabulary=0.60 + 0.25 * length_score,
            fluency=0.55 + 0.25 * length_score,
            comprehension=0.70 if text else 0.40,
            pronunciation=None,
        )
        confidence = 0.70 + (0.08 if has_connectors else 0)
        assessment = decide_promotion(
            CefrLevel.A1,
            scores,
            min(confidence, 1.0),
            f"Rubric reference: {CEFR_RUBRICS[CefrLevel.A1]} Evidence length={len(text.split())}, connectors={has_connectors}.",
        )
        return TutorResponse(
            session_id=str(uuid4()),
            agent_role=self.role,
            reply="I evaluated your latest performance and updated your level-readiness plan.",
            assessment=assessment,
        )
