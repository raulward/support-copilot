import uuid
from time import perf_counter
from typing import List

from app.core.logging import get_logger
from app.core.schemas import TicketInput, TicketOutput, Citation
from app.agents.specialist import specialist_generate, get_client
from app.rag.faiss_retriever import FaissRetriever

logger = get_logger()

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


    retriever = FaissRetriever(client=get_client())
    hits = retriever.retrieve(payload.message, top_k=3)

    context_chunks = [(h.chunk, h.score) for h in hits[:2]]


    citations: List[Citation] = [
        Citation(
            doc_id=h.chunk.doc_id,
            snippet=h.chunk.text[:300].strip(),
            score=float(round(h.score, 4)),
        )
        for h in hits
    ]

    logger.info(
        f"request_id={request_id} retriever=faiss retrieval_count={len(citations)} "
        f"retrieval_docs={[c.doc_id for c in citations]} scores={[round(c.score, 3) for c in citations]}"
    )

    llm_out = specialist_generate(
        ticket_message=payload.message,
        context_chunks=context_chunks,
        model="gpt-4o-mini",
    )

    draft_reply: str = llm_out.get(
        "draft_reply",
        "Recebemos seu chamado e já iniciamos a análise. Para avançar, poderia confirmar (1) ID/e-mail, (2) quando começou, e (3) passos para reproduzir?",
    )

    diagnostic_questions: List[str] = llm_out.get(
        "diagnostic_questions",
        [
            "Você pode informar o e-mail/ID do usuário afetado?",
            "Quando o problema começou e com que frequência acontece?",
            "Você consegue reproduzir? Se sim, quais passos?",
        ],
    )

    suggested_actions: List[str] = llm_out.get("suggested_actions", [])

    logger.info(f"request_id={request_id} specialist_model=gpt-4o-mini specialist_ok=True")

    summary = payload.message.strip()[:180]
    risk_flags: List[str] = []


    logger.info(f"request_id={request_id} specialist_model=gpt-4o-mini specialist_ok=True")

    risk_flags = []

    elapsed_ms = (perf_counter() - t0) * 1000
    usage = {
        "latency_ms": round(elapsed_ms, 2),
        "tokens": None,
        "cost_usd": None,
        "model": "gpt-4o-mini",
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
