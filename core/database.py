"""
Database setup for SQLAlchemy 2.0.
Provides the engine, sessionmaker, base class for models, and dependency to get a database session.
"""
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from core.config import settings

# Create SQLAlchemy engine.
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy declarative models.
    """
    pass

def get_db() -> Generator:
    """
    Dependency function to yield a database session.
    Closes the session after the request is finished.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
