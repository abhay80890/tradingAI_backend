import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from core.database import Base

class Document(Base):
    """Document model representing an uploaded file or source document."""
    __tablename__ = 'documents'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    issuer = Column(String)
    doc_type = Column(String)
    period = Column(String, nullable=True)
    source_uri = Column(String, nullable=True)
    status = Column(String, default='uploaded')
    file_size = Column(Integer)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    user = relationship("User", back_populates="documents")
    chunks = relationship("DocumentChunk", back_populates="document")

class DocumentChunk(Base):
    """DocumentChunk model representing a text fragment of a document."""
    __tablename__ = 'document_chunks'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey('documents.id'))
    text_content = Column(Text)
    embedding_ref = Column(String, nullable=True)
    page = Column(Integer, nullable=True)
    section = Column(String, nullable=True)

    # Relationships
    document = relationship("Document", back_populates="chunks")
