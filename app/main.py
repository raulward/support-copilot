from fastapi import FastAPI
from time import perf_counter
from app.core.schemas import TicketInput, TicketOutput

app = FastAPI(
    title='SupportCopilot',
    version="0.1.0",
    description="Multi-agent support copilot with RAG"
)

def fake_router(message: str):
    m = message.lower()
    if "senha" in m or "login" in m or "2fa" in m:
        return "Acesso/Conta", "P2", 0.90
    if "agendar" in m or "agenda" in m or "reagendar" in m:
        return "Agendamento", "P2", 0.85
    if "webhook" in m or "integra" in m or "crm" in m:
        return "Integrações", "P2", 0.80
    return "Atendimento Geral", "P3", 0.60


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ticket/analyze", response_model=TicketOutput)
def analyze_ticket(payload: TicketInput):
    t0 = perf_counter()

    category, priority, confidence = fake_router(payload.message)

    summary = payload.message.strip()[:160]

    diagnostic_questions = [
        "Qual é o e-mail/ID do usuário afetado?",
        "Quando o problema começou e com que frequência acontece?",
        "Você consegue reproduzir? Se sim, quais passos?",
    ]
    suggested_actions = [
        "Coletar logs/prints do erro",
        "Confirmar impacto (quantos usuários afetados)",
        "Aplicar procedimento padrão da categoria",
    ]
    draft_reply = (
        "Recebemos seu chamado e já iniciamos a análise. "
        "Para avançar rapidamente, poderia confirmar as informações solicitadas acima? "
        "Assim que tivermos retorno, seguimos com a resolução."
    )

    citations = []
    risk_flags = []

    elapsed_ms = (perf_counter() - t0) * 1000
    usage = {"latency_ms": round(elapsed_ms, 2), "tokens": None, "cost_usd": None}

    return TicketOutput(
        category=category,
        priority=priority,
        confidence=confidence,
        summary=summary,
        diagnostic_questions=diagnostic_questions,
        suggested_actions=suggested_actions,
        draft_reply=draft_reply,
        citations=citations,
        risk_flags=risk_flags,
        usage=usage,
    )
