import uuid
from datetime import datetime

from sqlalchemy import TIMESTAMP, Column, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ReviewInfo(Base):
    __tablename__ = 'notifications_reviewinfo'

    pkid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    movie_id = Column(UUID(as_uuid=True), default=uuid.uuid4)
    author_id = Column(UUID(as_uuid=True), default=uuid.uuid4)
    review_id = Column(UUID(as_uuid=True), default=uuid.uuid4)
    likes_count = Column(Integer, default=0)
    created = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)
    modified = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
