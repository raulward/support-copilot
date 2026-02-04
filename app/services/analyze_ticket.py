import uuid
from time import perf_counter
from typing import List, Tuple
from app.core.logging import get_logger
from app.core.schemas import TicketInput, TicketOutput
from app.rag.retriver import load_chunks, retriver
from app.core.schemas import Citation, Chunk
from app.agents.specialist import specialist_generate

logger = get_logger()

_KB_CHUNKS: List[Chunk] | None = None


def _get_kb_chunks() -> List[Chunk]:
    global _KB_CHUNKS
    if _KB_CHUNKS is None:
        _KB_CHUNKS = load_chunks()
    return _KB_CHUNKS



def _fake_router(message: str):

    m = message.lower()

    if any(k in m for k in ["senha", "login", "2fa", "autenticação", "acesso"]):
        return "Acesso/Conta", "P2", 0.90

    if any(k in m for k in ["agendar", "agenda", "reagendar", "horário", "calendário"]):
        return "Agendamento", "P2", 0.85

    if any(k in m for k in ["webhook", "integra", "crm", "api", "endpoint"]):
        return "Integrações", "P2", 0.80

    if any(k in m for k in ["instável", "fora do ar", "erro 500", "lento", "queda"]):
        return "Incidente", "P1", 0.75

    if any(k in m for k in ["cobrança", "fatura", "pagamento", "plano", "limite"]):
        return "Faturamento/Plano", "P2", 0.80

    return "Atendimento Geral", "P3", 0.60


def analyze_ticket_service(payload: TicketInput) -> TicketOutput:

    request_id = str(uuid.uuid4())

    t0 = perf_counter()

    logger.info(
        f"request_id={request_id} ticket_id={payload.ticket_id} channel={payload.channel}"
    )


    category, priority, confidence = _fake_router(payload.message)

    kb_chunks = _get_kb_chunks()
    retrieved = retriver(payload.message, kb_chunks, top_k=3, min_score=1)
    context_chunks = [(chunk, score) for chunk, score in retrieved][:2]


    citations: List[Citation] = []
    for chunk, score in retrieved:
        snippet = chunk.text[:280].strip()
        citations.append(Citation(doc_id=chunk.doc_id, snippet=snippet, score=float(score)))

    logger.info(
        f"request_id={request_id} retrieval_count={len(citations)} "
        f"retrieval_docs={[c.doc_id for c in citations]}"
    )

    llm_out = specialist_generate(
        ticket_message=payload.message,
        context_chunks=context_chunks,
        model="gpt-4o-mini",
    )


    suggested_actions = []

    if not citations:
        suggested_actions = [
            "Confirmar escopo/impacto (quantos usuários afetados)",
            "Coletar evidências (prints, logs, horário aproximado)",
            "Solicitar informações mínimas antes de aplicar um procedimento",
        ]

    summary = payload.message.strip()[:180]

    draft_reply = []
    diagnostic_questions = []

    draft_reply = llm_out.get("draft_reply", draft_reply)
    diagnostic_questions = llm_out.get("diagnostic_questions", diagnostic_questions)

    logger.info(f"request_id={request_id} specialist_model=gpt-4o-mini specialist_ok=True")

    risk_flags = []

    elapsed_ms = (perf_counter() - t0) * 1000
    usage = {
        "latency_ms": round(elapsed_ms, 2),
        "tokens": None,
        "cost_usd": None,
        "model": None,
        "fallback_used": False,
    }
    logger.info(
        f"request_id={request_id} category={category} priority={priority} confidence={confidence}"
    )


    return TicketOutput(
        request_id=request_id,
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
