from datetime import datetime
import uuid
from typing import Tuple, Optional

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.support_ticket import SupportTicket, TicketPriority

PRIORITY_MAP = {
    "emergency_sos":             TicketPriority.CRITICAL,
    "accident_report":           TicketPriority.CRITICAL,
    "ride_started_without_user": TicketPriority.CRITICAL,
    "driver_misbehavior":        TicketPriority.HIGH,
    "rash_driving":              TicketPriority.HIGH,
    "double_payment":            TicketPriority.HIGH,
    "report_driver":             TicketPriority.HIGH,
    "refund_not_received":       TicketPriority.NORMAL,
    "escalate_refund":           TicketPriority.NORMAL,
    "refund_initiated":          TicketPriority.NORMAL,
    "payment_failed":            TicketPriority.NORMAL,
    "cancel_ride_now":           TicketPriority.NORMAL,
    "cancellation_fee_issue":    TicketPriority.NORMAL,
    "lost_item":                 TicketPriority.NORMAL,
    "report_lost_item":          TicketPriority.NORMAL,
    "contact_support":           TicketPriority.NORMAL,
    "dispute_fare":              TicketPriority.NORMAL,
    "dispute_charge":            TicketPriority.NORMAL,
    "dispute_route":             TicketPriority.NORMAL,
    "login_problem":             TicketPriority.LOW,
    "apply_coupon":              TicketPriority.LOW,
}

TICKET_INTENTS = set(PRIORITY_MAP.keys())


def get_priority(intent: str) -> TicketPriority:
    return PRIORITY_MAP.get(intent, TicketPriority.NORMAL)


def generate_ticket_ref() -> str:
    now = datetime.utcnow()
    random_part = str(uuid.uuid4().int)[:5]
    return f"URB-{now.strftime('%Y%m')}-{random_part}"


def get_existing_ticket(db: Session, user_id: int, issue_type: str, ride_id: Optional[str] = None) -> Optional[SupportTicket]:
    """Check for an existing OPEN or IN_PROGRESS ticket for the same user and issue."""
    query = db.query(SupportTicket).filter(
        SupportTicket.user_id == user_id,
        SupportTicket.issue_type == issue_type,
        SupportTicket.status.in_(["OPEN", "IN_PROGRESS"])
    )
    if ride_id:
        query = query.filter(SupportTicket.ride_id == ride_id)
    return query.first()


def create_ticket(
    user_id: int,
    issue_type: str,
    issue_sub_type: str = "",
    detected_language: str = "en",
    confidence_score: float = 0.0,
    ride_id: str | None = None,
    driver_id: str | None = None,
    description: str = "",
) -> Tuple[SupportTicket, bool]:
    """
    Creates a new support ticket or returns an existing open one.
    Returns: (SupportTicket object, is_new flag)
    """
    db = SessionLocal()
    try:
        # Check for duplicate
        existing = get_existing_ticket(db, user_id, issue_type, ride_id)
        if existing:
            return existing, False

        # Create new if none found
        new_ticket = SupportTicket(
            id=str(uuid.uuid4()),
            ticket_ref=generate_ticket_ref(),
            user_id=user_id,
            ride_id=ride_id,
            driver_id=driver_id,
            issue_type=issue_type,
            issue_sub_type=issue_sub_type,
            description=description,
            detected_language=detected_language,
            confidence_score=confidence_score,
            channel="chatbot",
            priority=get_priority(issue_type),
        )

        db.add(new_ticket)
        db.commit()
        db.refresh(new_ticket)
        return new_ticket, True
    finally:
        db.close()
