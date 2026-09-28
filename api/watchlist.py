from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import get_current_user
from models.user import User
from models.watchlist import Watchlist
from models.security import Security
import uuid
from datetime import datetime
from services.audit_service import log_event

router = APIRouter(prefix='/api/v1/watchlist', tags=['watchlist'])

@router.get('/', response_model=dict)
def get_watchlist(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """List user's watchlist."""
    items = db.query(Watchlist, Security).join(Security, Watchlist.security_id == Security.id).filter(Watchlist.user_id == current_user.id).all()
    
    data = [
        {
            "id": str(wl.id),
            "added_at": wl.added_at.isoformat(),
            "security": {
                "id": str(sec.id),
                "symbol": sec.symbol,
                "name": sec.name
            }
        } for wl, sec in items
    ]
    
    return {
        "status": "success",
        "data": data,
        "message": "Watchlist retrieved"
    }

@router.post('/', response_model=dict)
def add_to_watchlist(security_id: str = Body(..., embed=True), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Add a security to the watchlist."""
    # Check if security exists
    sec = db.query(Security).filter(Security.id == security_id).first()
    if not sec:
        return {"status": "error", "error_code": "NOT_FOUND", "message": "Security not found"}
        
    # Check for duplicate
    existing = db.query(Watchlist).filter(Watchlist.user_id == current_user.id, Watchlist.security_id == security_id).first()
    if existing:
        return {"status": "error", "error_code": "DUPLICATE", "message": "Security already in watchlist"}
        
    # Add to watchlist
    wl_item = Watchlist(
        id=uuid.uuid4(),
        user_id=current_user.id,
        security_id=security_id,
        added_at=datetime.utcnow()
    )
    db.add(wl_item)
    db.commit()
    db.refresh(wl_item)
    
    log_event(db, current_user.id, "watchlist_add", "Watchlist", str(wl_item.id))
    
    return {
        "status": "success",
        "data": {"id": str(wl_item.id)},
        "message": "Added to watchlist"
    }

@router.delete('/{watchlist_id}', response_model=dict)
def remove_from_watchlist(watchlist_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Remove a security from the watchlist."""
    item = db.query(Watchlist).filter(Watchlist.id == watchlist_id, Watchlist.user_id == current_user.id).first()
    if not item:
        return {"status": "error", "error_code": "NOT_FOUND", "message": "Watchlist item not found"}
        
    db.delete(item)
    db.commit()
    
    log_event(db, current_user.id, "watchlist_remove", "Watchlist", watchlist_id)
    
    return {
        "status": "success",
        "data": None,
        "message": "Removed from watchlist"
    }
