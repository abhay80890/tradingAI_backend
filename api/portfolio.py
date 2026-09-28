from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import get_current_user
from models.user import User
from models.portfolio import Portfolio, Position
from models.security import Security
import uuid
from datetime import datetime
from services.audit_service import log_event

router = APIRouter(prefix='/api/v1/portfolios', tags=['portfolios'])

@router.get('/', response_model=dict)
def get_portfolios(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get user's portfolios and their positions."""
    portfolios = db.query(Portfolio).filter(Portfolio.user_id == current_user.id).all()
    
    data = []
    for p in portfolios:
        positions = db.query(Position, Security).join(Security, Position.security_id == Security.id).filter(Position.portfolio_id == p.id).all()
        pos_data = [
            {
                "id": str(pos.id),
                "symbol": sec.symbol,
                "quantity": pos.quantity,
                "avg_price": pos.avg_price
            } for pos, sec in positions
        ]
        
        data.append({
            "id": str(p.id),
            "name": p.name,
            "cash": p.cash,
            "risk_profile": p.risk_profile,
            "positions": pos_data
        })
        
    return {
        "status": "success",
        "data": data,
        "message": "Portfolios retrieved"
    }

@router.post('/', response_model=dict)
def create_portfolio(
    name: str = Body(..., embed=True), 
    initial_cash: float = Body(100000.0, embed=True),
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """Create a new portfolio."""
    portfolio = Portfolio(
        id=uuid.uuid4(),
        user_id=current_user.id,
        name=name,
        cash=initial_cash,
        created_at=datetime.utcnow()
    )
    db.add(portfolio)
    db.commit()
    db.refresh(portfolio)
    
    log_event(db, current_user.id, "portfolio_create", "Portfolio", str(portfolio.id))
    
    return {
        "status": "success",
        "data": {"id": str(portfolio.id), "name": portfolio.name, "cash": portfolio.cash},
        "message": "Portfolio created"
    }
