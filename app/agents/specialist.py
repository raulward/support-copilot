import json
from typing import List, Optional

from openai import OpenAI

from app.core.schemas import Citation

client = OpenAI()

def build_specialist_prompt(ticket_message: str, citations: List[Citation]) -> str:
    ctx = []

    for i, c in enumerate(citations, start=1):
        ctx.append(f"[{i}] doc_id={c.doc_id} score={c.score}\n{c.snippet}")

    context_block = "\n\n".join(ctx) if ctx else "(sem contexto recuperado)"

    return (
        """Você é um especialista de suporte técnico.
        Responda em português, tom profissional e direto.\n\n
        Regras:\n
        - Use APENAS o contexto fornecido em 'Contexto (KB)'.\n
        - Se o contexto não for suficiente, faça perguntas de diagnóstico e NÃO invente procedimento.\n
        - Não peça senha, código 2FA ou tokens.\n
        - Retorne SOMENTE um JSON válido, sem texto extra.\n\n
        Formato JSON esperado:\n
        {\n
          draft_reply": "string",\n
          diagnostic_questions": ["..."],\n
          suggested_actions": ["..."]\n
        }\n\n"
        f"Ticket:\n{ticket_message}\n\n"
        f"Contexto (KB):\n{context_block}\n"""
    )


def speacilist_generate(
        ticket_message: str,
        citations: List[Citation],
        model: str = "gpt-4o-mini"
) -> dict:

    prompt = build_specialist_prompt(ticket_message, citations)

    resp = client.responses.create(
        model = model,
        input = prompt,
        reasoning = {"effort": "low"}
    )

    text = resp.output_text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {
            "draft_reply": (
                "Recebemos seu chamado e já iniciamos a análise. "
                "Para avançar, poderia confirmar (1) ID/e-mail do usuário, (2) quando começou, "
                "e (3) passos para reproduzir? Assim seguimos com a orientação correta."
            ),
            "diagnostic_questions": [
                "Você pode informar o e-mail/ID do usuário afetado?",
                "Quando o problema começou e com que frequência acontece?",
                "Você consegue reproduzir? Se sim, quais passos?",
            ],
            "suggested_actions": [],
        }
