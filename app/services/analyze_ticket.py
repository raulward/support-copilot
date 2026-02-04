import uuid
from time import perf_counter
from app.core.logging import get_logger
from app.core.schemas import TicketInput, TicketOutput


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

    # Por enquanto: resumo simples (depois você troca por LLM)
    summary = payload.message.strip()[:180]

    diagnostic_questions = [
        "Você pode informar o e-mail/ID do usuário afetado?",
        "Quando o problema começou e com que frequência acontece?",
        "Você consegue reproduzir? Se sim, quais passos?",
    ]

    suggested_actions = [
        "Confirmar escopo/impacto (quantos usuários afetados)",
        "Coletar evidências (prints, logs, horário aproximado)",
        "Aplicar procedimento padrão da categoria e validar a resolução",
    ]

    draft_reply = (
        "Recebemos seu chamado e já iniciamos a análise. "
        "Para avançar mais rápido, poderia confirmar: (1) ID/e-mail do usuário, "
        "(2) quando começou, e (3) passos para reproduzir? "
        "Com isso, seguimos com a solução e te atualizamos com o próximo passo."
    )

    citations = []   # RAG vai preencher
    risk_flags = []  # Guard Agent vai preencher

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
