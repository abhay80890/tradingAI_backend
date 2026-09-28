from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import get_current_user
from models.user import User
from models.research import ResearchJob
from models.security import Security
import uuid
from datetime import datetime
from services.audit_service import log_event
from typing import Optional

router = APIRouter(prefix='/api/v1/research', tags=['research'])

@router.post('/', response_model=dict)
def create_research_job(
    symbol: str = Body(..., embed=True),
    custom_prompt: Optional[str] = Body(None, embed=True),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new research job."""
    # Find security
    sec = db.query(Security).filter(Security.symbol.ilike(symbol)).first()
    if not sec:
        return {"status": "error", "error_code": "NOT_FOUND", "message": f"Security {symbol} not found"}
        
    correlation_id = str(uuid.uuid4())
    
    job = ResearchJob(
        id=uuid.uuid4(),
        user_id=current_user.id,
        security_id=sec.id,
        status="pending",
        correlation_id=correlation_id,
        created_at=datetime.utcnow()
    )
    # custom_prompt would be saved or passed to the worker here, but standard model lacks it
    
    db.add(job)
    db.commit()
    db.refresh(job)
    
    log_event(db, current_user.id, "research_job_create", "ResearchJob", str(job.id))
    
    # In a real app, we would enqueue a Celery task here using the correlation_id
    
    return {
        "status": "success",
        "data": {"job_id": str(job.id), "correlation_id": correlation_id},
        "message": "Research job created"
    }

@router.get('/{job_id}', response_model=dict)
def get_research_job(job_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get research job details."""
    job = db.query(ResearchJob).filter(ResearchJob.id == job_id, ResearchJob.user_id == current_user.id).first()
    
    if not job:
         return {"status": "error", "error_code": "NOT_FOUND", "message": "Research job not found"}
         
    return {
        "status": "success",
        "data": {
            "id": str(job.id),
            "status": job.status,
            "correlation_id": job.correlation_id,
            "created_at": job.created_at.isoformat()
        },
        "message": "Research job retrieved"
    }

@router.get('/{job_id}/status', response_model=dict)
def get_research_job_status(job_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get just the status of a research job."""
    job = db.query(ResearchJob).filter(ResearchJob.id == job_id, ResearchJob.user_id == current_user.id).first()
    
    if not job:
         return {"status": "error", "error_code": "NOT_FOUND", "message": "Research job not found"}
         
    return {
        "status": "success",
        "data": {
            "id": str(job.id),
            "status": job.status
        },
        "message": "Research job status retrieved"
    }
