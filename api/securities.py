from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from models.security import Security
from typing import Optional

router = APIRouter(prefix='/api/v1/securities', tags=['securities'])

@router.get('/search', response_model=dict)
def search_securities(q: str, db: Session = Depends(get_db)):
    """Search securities by symbol or name."""
    search_term = f"%{q}%"
    securities = db.query(Security).filter(
        (Security.symbol.ilike(search_term)) | (Security.name.ilike(search_term))
    ).limit(20).all()
    
    data = [
        {"id": str(sec.id), "symbol": sec.symbol, "name": sec.name, "exchange": sec.exchange}
        for sec in securities
    ]
    
    return {
        "status": "success",
        "data": data,
        "message": "Securities retrieved"
    }

@router.get('/{security_id}', response_model=dict)
def get_security(security_id: str, db: Session = Depends(get_db)):
    """Get a single security by ID."""
    sec = db.query(Security).filter(Security.id == security_id).first()
    if not sec:
        return {"status": "error", "error_code": "NOT_FOUND", "message": "Security not found"}
        
    data = {
        "id": str(sec.id), "symbol": sec.symbol, "name": sec.name, 
        "exchange": sec.exchange, "sector": sec.sector, "currency": sec.currency
    }
    
    return {
        "status": "success",
        "data": data,
        "message": "Security retrieved"
    }
