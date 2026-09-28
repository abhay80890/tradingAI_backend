from sqlalchemy.orm import Session
from models.audit import AuditEvent
import uuid
from datetime import datetime
from typing import Optional

def log_event(db: Session, user_id: uuid.UUID, action: str, entity_type: Optional[str] = None, entity_id: Optional[str] = None) -> AuditEvent:
    """
    Log an audit event to the database.
    
    Args:
        db: SQLAlchemy session
        user_id: The ID of the user performing the action
        action: String describing the action (e.g., 'user_login', 'order_buy')
        entity_type: Optional type of entity affected (e.g., 'Order', 'Portfolio')
        entity_id: Optional ID of the entity affected
        
    Returns:
        The created AuditEvent object
    """
    event = AuditEvent(
        id=uuid.uuid4(),
        user_id=user_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        timestamp=datetime.utcnow()
    )
    
    db.add(event)
    # Don't commit here, let the calling transaction handle it
    # But if we need it standalone, we could commit
    
    return event
