import json
import os
from typing import List, Optional, Tuple
from openai import OpenAI
from app.core.schemas import Citation, Chunk



_client: OpenAI | None = None

def get_client() -> OpenAI:
    global _client
    if _client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY não configurada.")
        _client = OpenAI(api_key=api_key)
    return _client


def build_specialist_prompt(
    ticket_message: str,
    context_chunks: List[Tuple[Chunk, float]],
) -> str:
    ctx = []
    for i, (ch, score) in enumerate(context_chunks, start=1):
        text = ch.text[:1800].strip()
        ctx.append(f"[{i}] doc_id={ch.doc_id} chunk_id={ch.chunk_id} score={score}\n{text}")

    context_block = "\n\n".join(ctx) if ctx else "(sem contexto recuperado)"

    return (
        "Você é um especialista de suporte técnico.\n"
        "Responda em português, tom profissional e direto.\n\n"
        "Regras obrigatórias:\n"
        "1) Se houver 'Contexto (KB)' (não vazio), você DEVE:\n"
        "   - Incluir 2 ou 3 orientações concretas extraídas do KB (procedimento/ações).\n"
        "   - Fazer no máximo 3 perguntas de diagnóstico, preferindo as do KB.\n"
        "2) Se NÃO houver contexto suficiente, você deve apenas:\n"
        "   - Fazer no máximo 3 perguntas de diagnóstico.\n"
        "   - Não sugerir procedimento específico.\n"
        "3) Nunca peça senha, código 2FA ou tokens.\n"
        "4) suggested_actions deve ter pelo menos 2 itens quando houver KB.\n"
        "5) não repita as perguntas no draft_reply; retorne-as apenas em diagnostic_questions\n"
        "6) Retorne SOMENTE o JSON que segue o schema.\n"
        "7) NÃO escreva as perguntas dentro de draft_reply. Deixe perguntas apenas em diagnostic_questions.\n"
        f"Ticket:\n{ticket_message}\n\n"
        f"Contexto (KB):\n{context_block}\n"
    )



def specialist_generate(
        ticket_message: str,
        context_chunks: List[Tuple[Chunk, int]],
        model: str = "gpt-4o-mini"
) -> dict:

    client = get_client()

    prompt = build_specialist_prompt(ticket_message, context_chunks)

    resp = client.responses.create(
        model=model,
        input=prompt,
        text={
            "format": {
                "type": "json_schema",
                "name": "SupportReply",
                "schema": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "draft_reply": {"type": "string"},
                        "diagnostic_questions": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                        "suggested_actions": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                    },
                    "required": ["draft_reply", "diagnostic_questions", "suggested_actions"],
                },
            }
        },
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
