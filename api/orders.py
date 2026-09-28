from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import get_current_user
from models.user import User
from models.order import Order
from models.portfolio import Portfolio, Position
from schemas.trading import OrderCreate
from services.trading_service import execute_paper_order
from services.audit_service import log_event
from models.security import Security
from datetime import datetime

router = APIRouter(prefix='/api/v1/orders', tags=['orders'])

@router.post('/', response_model=dict)
def place_order(
    order_data: OrderCreate,
    portfolio_id: str = Body(..., embed=True),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Place a paper trading order."""
    # Verify portfolio belongs to user
    portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id, Portfolio.user_id == current_user.id).first()
    if not portfolio:
        return {"status": "error", "error_code": "NOT_FOUND", "message": "Portfolio not found"}
        
    # Placeholder price logic - in a real app, integrate Alpha Vantage here
    current_price = 150.0 
    
    try:
        # Execute the order via service
        order = execute_paper_order(
            db=db,
            portfolio_id=portfolio.id,
            symbol=order_data.symbol,
            side=order_data.side,
            qty=order_data.quantity,
            price=current_price,
            idempotency_key=order_data.idempotency_key
        )
        
        log_event(db, current_user.id, f"order_{order_data.side}", "Order", str(order.id))
        
        return {
            "status": "success",
            "data": {
                "id": str(order.id),
                "symbol": order_data.symbol,
                "side": order.side,
                "qty": order.qty,
                "price": order.price,
                "status": order.status
            },
            "message": "Order executed successfully"
        }
    except ValueError as e:
        return {"status": "error", "error_code": "BAD_REQUEST", "message": str(e)}

@router.get('/', response_model=dict)
def get_order_history(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """List user's order history."""
    # Find user's portfolios
    portfolio_ids = [p.id for p in db.query(Portfolio.id).filter(Portfolio.user_id == current_user.id).all()]
    
    if not portfolio_ids:
         return {"status": "success", "data": [], "message": "No portfolios found"}
         
    orders = db.query(Order, Security).join(Security, Order.security_id == Security.id).filter(Order.portfolio_id.in_(portfolio_ids)).order_by(Order.created_at.desc()).all()
    
    data = [
        {
            "id": str(o.id),
            "portfolio_id": str(o.portfolio_id),
            "symbol": sec.symbol,
            "side": o.side,
            "qty": o.qty,
            "price": o.price,
            "status": o.status,
            "created_at": o.created_at.isoformat()
        } for o, sec in orders
    ]
    
    return {
        "status": "success",
        "data": data,
        "message": "Order history retrieved"
    }

@router.get('/positions', response_model=dict)
def get_all_positions(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """List all positions across all portfolios for a user."""
    portfolio_ids = [p.id for p in db.query(Portfolio.id).filter(Portfolio.user_id == current_user.id).all()]
    
    if not portfolio_ids:
         return {"status": "success", "data": [], "message": "No portfolios found"}
         
    positions = db.query(Position, Security, Portfolio).join(Security, Position.security_id == Security.id).join(Portfolio, Position.portfolio_id == Portfolio.id).filter(Position.portfolio_id.in_(portfolio_ids)).all()
    
    data = [
        {
            "id": str(pos.id),
            "portfolio_id": str(port.id),
            "portfolio_name": port.name,
            "symbol": sec.symbol,
            "quantity": pos.quantity,
            "avg_price": pos.avg_price
        } for pos, sec, port in positions
    ]
    
    return {
        "status": "success",
        "data": data,
        "message": "Positions retrieved"
    }
