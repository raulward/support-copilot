from pydantic import BaseModel
from dataclasses import dataclass

class TicketInput(BaseModel):
    ticket_id: str
    message: str
    channel: str

class Citation(BaseModel):
    doc_id: str
    snippet: str
    score: int


class TicketOutput(BaseModel):

    request_id: str

    category: str
    priority: str
    confidence: float

    summary: str
    diagnostic_questions: list[str]
    suggested_actions: list[str]
    draft_reply: str

    citations: list[dict]
    risk_flags: list[str]

    usage: dict


@dataclass
class Chunk:
    doc_id: str
    chunk_id: str
    text: str
