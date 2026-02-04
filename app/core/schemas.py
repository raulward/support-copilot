from pydantic import BaseModel

class TicketInput(BaseModel):
    ticket_id: str
    message: str
    channel: str


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
