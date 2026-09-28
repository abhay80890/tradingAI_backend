import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from core.database import Base

class Order(Base):
    """Order model representing a trade order for a portfolio."""
    __tablename__ = 'orders'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id = Column(UUID(as_uuid=True), ForeignKey('portfolios.id'))
    security_id = Column(UUID(as_uuid=True), ForeignKey('securities.id'))
    side = Column(String) # 'buy' or 'sell'
    qty = Column(Integer)
    price = Column(Float)
    status = Column(String, default='executed')
    idempotency_key = Column(String, unique=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    portfolio = relationship("Portfolio", back_populates="orders")
    security = relationship("Security")
    transaction = relationship("Transaction", uselist=False, back_populates="order")

class Transaction(Base):
    """Transaction model representing the monetary impact of an order."""
    __tablename__ = 'transactions'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id = Column(UUID(as_uuid=True), ForeignKey('portfolios.id'))
    order_id = Column(UUID(as_uuid=True), ForeignKey('orders.id'))
    amount = Column(Float)
    balance_after = Column(Float)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    portfolio = relationship("Portfolio", back_populates="transactions")
    order = relationship("Order", back_populates="transaction")
