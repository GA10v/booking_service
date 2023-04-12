import enum
import uuid
from datetime import datetime

from sqlalchemy import TIMESTAMP, Column, Enum, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class EventType(enum.Enum):
    welcome = 'welcome_message'
    new_content = 'new_content'
    new_score = 'new_likes'
    promo = 'promo'

    announce_new = 'announce_new'
    announce_put = 'announce_put'
    announce_done = 'announce_done'
    announce_delete = 'announce_delete'

    booking_new = 'booking_new'
    booking_status = 'booking_status'
    booking_delete = 'booking_delete'


class Template(Base):
    __tablename__ = 'notifications_template'

    pkid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String(256), unique=True)
    event_type = Column(Enum(EventType))
    subject = Column(String(256), nullable=False)
    template_files = Column(String, nullable=False)
    text_msg = Column(String(4096), unique=True)
    created = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)
    modified = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
