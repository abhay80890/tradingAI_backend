import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from core.database import Base

class Portfolio(Base):
    """Portfolio model representing a user's investment portfolio."""
    __tablename__ = 'portfolios'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    name = Column(String, default='Default Portfolio')
    cash = Column(Float, default=100000.00)
    risk_profile = Column(String, default='moderate')
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    user = relationship("User", back_populates="portfolios")
    positions = relationship("Position", back_populates="portfolio")
    orders = relationship("Order", back_populates="portfolio")
    transactions = relationship("Transaction", back_populates="portfolio")

class Position(Base):
    """Position model representing an asset holding in a portfolio."""
    __tablename__ = 'positions'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id = Column(UUID(as_uuid=True), ForeignKey('portfolios.id'))
    security_id = Column(UUID(as_uuid=True), ForeignKey('securities.id'))
    quantity = Column(Integer, default=0)
    avg_price = Column(Float, default=0.0)

    __table_args__ = (
        UniqueConstraint('portfolio_id', 'security_id', name='uix_portfolio_security'),
    )

    # Relationships
    portfolio = relationship("Portfolio", back_populates="positions")
    security = relationship("Security")
