import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from core.database import Base

class Security(Base):
    """Security model representing a stock or other tradable asset."""
    __tablename__ = 'securities'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    symbol = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    exchange = Column(String, nullable=True)
    sector = Column(String, nullable=True)
    currency = Column(String, default='USD')
