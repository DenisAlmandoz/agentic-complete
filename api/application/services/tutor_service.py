from __future__ import annotations

from uuid import uuid4

from api.application.agents.language_agents import CoordinatorAgent, ExaminerAgent, PlannerAgent, ReadinessAssessorAgent, TeacherAgent
from api.domain.models import AgentRole, TutorRequest, TutorResponse
from api.infrastructure.memory.mongo_memory import MongoMemoryStore
from api.infrastructure.observability.langfuse_tracing import LangfuseTracer
from api.infrastructure.speech.whisper import WhisperTranscriber


class TutorService:
    def __init__(
        self,
        coordinator: CoordinatorAgent,
        planner: PlannerAgent,
        teacher: TeacherAgent,
        examiner: ExaminerAgent,
        readiness_assessor: ReadinessAssessorAgent,
        memory: MongoMemoryStore,
        transcriber: WhisperTranscriber,
        tracer: LangfuseTracer,
    ) -> None:
        self.coordinator = coordinator
        self.agents = {
            AgentRole.PLANNER: planner,
            AgentRole.TEACHER: teacher,
            AgentRole.EXAMINER: examiner,
            AgentRole.READINESS_ASSESSOR: readiness_assessor,
        }
        self.memory = memory
        self.transcriber = transcriber
        self.tracer = tracer

    def handle_turn(self, request: TutorRequest) -> TutorResponse:
        session_id = str(uuid4())
        if request.audio_base64 and not request.message:
            request.message = self.transcriber.transcribe_base64(request.audio_base64)

        with self.tracer.trace("language_tutor_turn", user_id=request.user_id, topic=request.topic):
            context = self.memory.retrieve_knowledge(
                query=request.message or request.topic,
                language=request.target_language.value,
                topic=request.topic,
            )
            role = self.coordinator.select_role(request)
            response = self.agents[role].run(request, context)
            response.session_id = session_id
            self.memory.remember_turn(
                request.user_id,
                session_id,
                request.message or "",
                {"agent": role.value, "topic": request.topic, "target_language": request.target_language.value},
            )
            return response

