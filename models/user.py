import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from core.database import Base

class User(Base):
    """User model representing a system user."""
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    risk_preference = Column(String, nullable=True, default='moderate')
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    watchlist_items = relationship("Watchlist", back_populates="user")
    research_jobs = relationship("ResearchJob", back_populates="user")
    portfolios = relationship("Portfolio", back_populates="user")
    documents = relationship("Document", back_populates="user")
