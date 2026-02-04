from fastapi import FastAPI
from app.api.tickets import router as tickets_router

app = FastAPI(
    title="SupportCopilot",
    version="0.1.0",
    description="Support ticket copilot (multi-agent + RAG), using Algarys-like context.",
)

app.include_router(tickets_router)


@app.get("/health")
def health():
    return {"status": "ok"}
