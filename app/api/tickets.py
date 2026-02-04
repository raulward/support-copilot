from fastapi import APIRouter
from app.core.schemas import TicketInput, TicketOutput
from app.services.analyze_ticket import analyze_ticket_service

router = APIRouter(prefix="/ticket", tags=["tickets"])


@router.post("/analyze", response_model=TicketOutput)
def analyze_ticket(payload: TicketInput) -> TicketOutput:
    return analyze_ticket_service(payload)
