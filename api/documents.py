from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import get_current_user
from models.user import User
from models.document import Document
import uuid
import os
import shutil
from datetime import datetime
from services.audit_service import log_event

router = APIRouter(prefix='/api/v1/documents', tags=['documents'])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post('/', response_model=dict)
async def upload_document(
    file: UploadFile = File(...),
    issuer: str = "",
    doc_type: str = "general",
    period: str = "",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Upload a document and store its metadata."""
    file_id = str(uuid.uuid4())
    file_ext = os.path.splitext(file.filename)[1]
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}{file_ext}")
    
    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    file_size = os.path.getsize(file_path)
    
    # Create DB record
    doc = Document(
        id=uuid.UUID(file_id),
        user_id=current_user.id,
        issuer=issuer,
        doc_type=doc_type,
        period=period,
        source_uri=file_path,
        status="uploaded",
        file_size=file_size,
        created_at=datetime.utcnow()
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    
    log_event(db, current_user.id, "document_upload", "Document", str(doc.id))
    
    return {
        "status": "success",
        "data": {"id": str(doc.id), "filename": file.filename},
        "message": "Document uploaded successfully"
    }

@router.get('/', response_model=dict)
def list_documents(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """List all non-deleted user documents."""
    docs = db.query(Document).filter(
        Document.user_id == current_user.id,
        Document.is_deleted == False
    ).order_by(Document.created_at.desc()).all()
    
    data = [
        {
            "id": str(doc.id),
            "issuer": doc.issuer,
            "doc_type": doc.doc_type,
            "period": doc.period,
            "status": doc.status,
            "file_size": doc.file_size,
            "created_at": doc.created_at.isoformat()
        } for doc in docs
    ]
    
    return {
        "status": "success",
        "data": data,
        "message": "Documents retrieved"
    }

@router.delete('/{document_id}', response_model=dict)
def delete_document(document_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Soft delete a document."""
    doc = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == current_user.id
    ).first()
    
    if not doc or doc.is_deleted:
        return {"status": "error", "error_code": "NOT_FOUND", "message": "Document not found"}
        
    doc.is_deleted = True
    db.commit()
    
    log_event(db, current_user.id, "document_delete", "Document", document_id)
    
    return {
        "status": "success",
        "data": None,
        "message": "Document deleted"
    }
