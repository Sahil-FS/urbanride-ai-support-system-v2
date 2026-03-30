from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.support_ticket import SupportTicket, TicketStatus
from app.services.cron_service import escalate_old_tickets

router = APIRouter(prefix="/admin/tickets", tags=["Admin Tickets"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ✅ GET ALL / FILTER TICKETS
@router.get("/")
def get_tickets(
    status: Optional[TicketStatus] = Query(None),
    priority: Optional[str] = Query(None),
):
    db: Session = SessionLocal()
    try:
        query = db.query(SupportTicket)

        if status:
            query = query.filter(SupportTicket.status == status)

        if priority:
            query = query.filter(SupportTicket.priority == priority)

        tickets = query.order_by(SupportTicket.created_at.desc()).all()

        return tickets
    finally:
        db.close()


# ✅ GET SINGLE TICKET
@router.get("/{ticket_id}")
def get_ticket(ticket_id: str):
    db: Session = SessionLocal()
    try:
        ticket = db.query(SupportTicket).filter(SupportTicket.id == ticket_id).first()

        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")

        return ticket
    finally:
        db.close()


# ✅ UPDATE TICKET STATUS
@router.patch("/{ticket_id}/status")
def update_ticket_status(ticket_id: str, status: TicketStatus):
    db: Session = SessionLocal()
    try:
        ticket = db.query(SupportTicket).filter(SupportTicket.id == ticket_id).first()

        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")

        ticket.status = status
        db.commit()
        db.refresh(ticket)

        return {
            "message": "Ticket status updated",
            "ticket_id": ticket.id,
            "new_status": ticket.status
        }
    finally:
        db.close()


# ✅ MANUAL ESCALATION TRIGGER
@router.post("/run-escalation")
def run_escalation():
    """Manual trigger to run the 7-day escalation logic."""
    escalate_old_tickets()
    return {"message": "Escalation job executed manually"}
