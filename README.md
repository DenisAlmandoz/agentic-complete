# Agentic Language Voice Tutor

A full-stack starter for an agentic RAG, multi-agent language-learning assistant that starts with English and Spanish. The backend is FastAPI/Python with clean `domain`, `application`, and `infrastructure` layers. The UI is a lightweight JavaScript app that can talk to the API, choose a target language/topic, submit text or audio, and review level-readiness feedback.

## Architecture

```text
api/
  domain/             # CEFR, lesson, assessment, and conversation models
  application/        # multi-agent orchestration, use cases, evals
  infrastructure/     # Grok/xAI, MongoDB memory/vector search, Whisper, Langfuse
ui/                   # frontend JavaScript app
```

## Capabilities

- Grok LLM via the xAI OpenAI-compatible Chat Completions API (`https://api.x.ai/v1`).
- Multi-agent flow: coordinator, planner, retrieval/teacher, examiner, and readiness assessor.
- Agentic RAG with MongoDB Atlas Vector Search-compatible abstractions for external learning material, short-term memory, and long-term memory.
- Voice input through a Whisper-compatible transcriber abstraction.
- Langfuse tracing hooks for LLM calls and learning sessions.
- Evals for CEFR promotion decisions, rubric consistency, and Spanish/English tutoring quality.

## Quick start

```bash
cp .env.example .env
python -m venv .venv
source .venv/bin/activate
poetry install
poetry run uvicorn api.main:app --reload

# Or, if you prefer pip:
pip install -r api/requirements.txt
uvicorn api.main:app --reload
```

Then open `ui/index.html` in a browser or serve it with any static file server.

## Environment

See `.env.example` for all configuration. The app is designed to run locally with MongoDB Atlas or a local MongoDB instance, and can be wired to Langfuse Cloud or self-hosted Langfuse.

