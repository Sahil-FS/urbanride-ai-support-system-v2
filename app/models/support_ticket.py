from sqlalchemy import Column, String, Integer, Text, DateTime, Enum, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum
import uuid

Base = declarative_base()


class TicketStatus(str, enum.Enum):
    OPEN        = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    ESCALATED   = "ESCALATED"
    RESOLVED    = "RESOLVED"
    CLOSED      = "CLOSED"


class TicketPriority(str, enum.Enum):
    LOW      = "LOW"
    NORMAL   = "NORMAL"
    HIGH     = "HIGH"
    CRITICAL = "CRITICAL"


class SupportTicket(Base):
    __tablename__ = "support_tickets"

    id                = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    ticket_ref        = Column(String(20), unique=True, nullable=False)
    user_id           = Column(Integer, nullable=False)
    ride_id           = Column(String(36), nullable=True)
    driver_id         = Column(String(36), nullable=True)
    issue_type        = Column(String(50), nullable=False)
    issue_sub_type    = Column(String(50), nullable=True)
    description       = Column(Text, nullable=True)
    detected_language = Column(String(10), default="en")
    confidence_score  = Column(Float, nullable=True)
    channel           = Column(String(20), default="chatbot")
    status            = Column(Enum(TicketStatus), default=TicketStatus.OPEN, nullable=False)
    priority          = Column(Enum(TicketPriority), default=TicketPriority.NORMAL, nullable=False)
    resolution_note   = Column(Text, nullable=True)
    created_at        = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at        = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at       = Column(DateTime, nullable=True)
