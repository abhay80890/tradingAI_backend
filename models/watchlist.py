import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from core.database import Base

class Watchlist(Base):
    """Watchlist model representing a user's watched securities."""
    __tablename__ = 'watchlist'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    security_id = Column(UUID(as_uuid=True), ForeignKey('securities.id'))
    added_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        UniqueConstraint('user_id', 'security_id', name='uix_user_security'),
    )

    # Relationships
    user = relationship("User", back_populates="watchlist_items")
    security = relationship("Security")
