import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from core.database import Base

class ResearchJob(Base):
    """ResearchJob model representing an analysis job for a security."""
    __tablename__ = 'research_jobs'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    security_id = Column(UUID(as_uuid=True), ForeignKey('securities.id'))
    status = Column(String, default='pending')
    correlation_id = Column(String, unique=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    user = relationship("User", back_populates="research_jobs")
    security = relationship("Security")
    runs = relationship("AgentRun", back_populates="job")
    report = relationship("Report", uselist=False, back_populates="job")

class AgentRun(Base):
    """AgentRun model representing a specific agent execution within a job."""
    __tablename__ = 'agent_runs'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_id = Column(UUID(as_uuid=True), ForeignKey('research_jobs.id'))
    agent_name = Column(String)
    status = Column(String)
    duration_ms = Column(Integer, nullable=True)
    output_summary = Column(Text, nullable=True)
    error_log = Column(Text, nullable=True)

    # Relationships
    job = relationship("ResearchJob", back_populates="runs")

class Report(Base):
    """Report model representing the final output of a research job."""
    __tablename__ = 'reports'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_id = Column(UUID(as_uuid=True), ForeignKey('research_jobs.id'), unique=True)
    content = Column(Text)
    version = Column(String, default='1.0')
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    job = relationship("ResearchJob", back_populates="report")
