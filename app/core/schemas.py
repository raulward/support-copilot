from pydantic import BaseModel

class TicketInput(BaseModel):
    ticket_id: str
    message: str
    channel: str


class TicketOutput(BaseModel):
    category: str
    priority: str
    confidence: float

    summary: str
    diagnostic_questions: list[str]
    suggested_action: list[str]
    draft_reply: str

    citations: list[dict]
    risk_flags: list[str]

    usage: dict

    
