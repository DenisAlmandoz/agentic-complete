from __future__ import annotations

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.application.agents.language_agents import CoordinatorAgent, ExaminerAgent, PlannerAgent, ReadinessAssessorAgent, TeacherAgent
from api.application.settings import Settings, get_settings
from api.application.services.tutor_service import TutorService
from api.domain.models import TutorRequest, TutorResponse
from api.infrastructure.llm.grok_client import GrokClient
from api.infrastructure.memory.mongo_memory import MongoMemoryStore
from api.infrastructure.observability.langfuse_tracing import LangfuseTracer
from api.infrastructure.speech.whisper import WhisperTranscriber

app = FastAPI(title="Agentic Language Voice Tutor", version="0.1.0")
settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def build_tutor_service(settings: Settings = Depends(get_settings)) -> TutorService:
    grok = GrokClient(settings)
    return TutorService(
        coordinator=CoordinatorAgent(),
        planner=PlannerAgent(),
        teacher=TeacherAgent(grok),
        examiner=ExaminerAgent(),
        readiness_assessor=ReadinessAssessorAgent(),
        memory=MongoMemoryStore(settings),
        transcriber=WhisperTranscriber(settings.whisper_model),
        tracer=LangfuseTracer(settings),
    )


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/tutor/turn", response_model=TutorResponse)
def tutor_turn(request: TutorRequest, service: TutorService = Depends(build_tutor_service)) -> TutorResponse:
    return service.handle_turn(request)
