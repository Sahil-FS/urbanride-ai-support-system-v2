from datetime import datetime, timedelta
from app.db.session import SessionLocal
from app.models.support_ticket import SupportTicket, TicketStatus, TicketPriority
import logging

logger = logging.getLogger(__name__)


def escalate_old_tickets():
    db = SessionLocal()

    try:
        threshold_date = datetime.utcnow() - timedelta(days=7)

        tickets = db.query(SupportTicket).filter(
            SupportTicket.status.in_([TicketStatus.OPEN, TicketStatus.IN_PROGRESS]),
            SupportTicket.priority != TicketPriority.CRITICAL,
            SupportTicket.created_at < threshold_date
        ).all()

        if not tickets:
            logger.info("[CRON] No tickets to escalate")
            return

        for ticket in tickets:
            ticket.priority = TicketPriority.CRITICAL
            ticket.status = TicketStatus.ESCALATED

        db.commit()

        logger.info(f"[CRON] Escalated {len(tickets)} tickets")

    except Exception as e:
        logger.error(f"[CRON ERROR] {str(e)}")

    finally:
        db.close()
