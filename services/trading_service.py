from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.order import Order
from models.portfolio import Portfolio, Position
from models.security import Security
import uuid
from datetime import datetime

def execute_paper_order(db: Session, portfolio_id: uuid.UUID, symbol: str, side: str, qty: int, price: float, idempotency_key: str) -> Order:
    """
    Execute a paper trading order atomically.
    
    Args:
        db: SQLAlchemy session
        portfolio_id: Portfolio UUID
        symbol: Security ticker symbol
        side: 'buy' or 'sell'
        qty: Number of shares
        price: Execution price
        idempotency_key: Unique key to prevent double execution
        
    Returns:
        Order object if successful
        
    Raises:
        ValueError: If validation fails
    """
    # 1. Check idempotency key to prevent double processing
    existing_order = db.query(Order).filter(Order.idempotency_key == idempotency_key).first()
    if existing_order:
        return existing_order
        
    # 2. Find security
    sec = db.query(Security).filter(Security.symbol.ilike(symbol)).first()
    if not sec:
        raise ValueError(f"Security with symbol {symbol} not found")
        
    # 3. Get portfolio
    # Use with_for_update to lock the row during transaction
    portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).with_for_update().first()
    if not portfolio:
        raise ValueError("Portfolio not found")
        
    total_value = qty * price
    
    # 4. Get or create position
    position = db.query(Position).filter(
        Position.portfolio_id == portfolio_id,
        Position.security_id == sec.id
    ).with_for_update().first()
    
    # 5. Process based on side
    if side == 'buy':
        if portfolio.cash < total_value:
            raise ValueError(f"Insufficient funds. Required: {total_value}, Available: {portfolio.cash}")
            
        # Deduct cash
        portfolio.cash -= total_value
        
        # Update position
        if position:
            new_qty = position.quantity + qty
            # Calculate new average price
            position.avg_price = ((position.quantity * position.avg_price) + total_value) / new_qty
            position.quantity = new_qty
        else:
            position = Position(
                id=uuid.uuid4(),
                portfolio_id=portfolio_id,
                security_id=sec.id,
                quantity=qty,
                avg_price=price
            )
            db.add(position)
            
    elif side == 'sell':
        if not position or position.quantity < qty:
            available = position.quantity if position else 0
            raise ValueError(f"Insufficient position. Requested: {qty}, Available: {available}")
            
        # Add cash
        portfolio.cash += total_value
        
        # Update position
        position.quantity -= qty
        if position.quantity == 0:
            db.delete(position)
    else:
        raise ValueError(f"Invalid side: {side}")
        
    # 6. Create Order record
    order = Order(
        id=uuid.uuid4(),
        portfolio_id=portfolio_id,
        security_id=sec.id,
        side=side,
        qty=qty,
        price=price,
        status="filled",
        idempotency_key=idempotency_key,
        created_at=datetime.utcnow()
    )
    db.add(order)
    
    try:
        db.commit()
        db.refresh(order)
        return order
    except IntegrityError:
        db.rollback()
        raise ValueError("Transaction failed due to concurrent modification or duplicate request")
