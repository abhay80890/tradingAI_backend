from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import hash_password, verify_password, create_access_token, get_current_user
from models.user import User
from schemas.auth import UserRegister, UserLogin, UserResponse, TokenResponse
from services.audit_service import log_event
import uuid
from datetime import datetime

router = APIRouter(prefix='/api/v1/auth', tags=['auth'])

@router.post('/register', response_model=dict, status_code=status.HTTP_201_CREATED)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """Register a new user."""
    # Check if user exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        return {"status": "error", "error_code": "USER_EXISTS", "message": "Email already registered"}
    
    # Create new user
    hashed_pw = hash_password(user_data.password)
    new_user = User(
        id=uuid.uuid4(),
        email=user_data.email,
        password_hash=hashed_pw,
        created_at=datetime.utcnow()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Log event
    log_event(db, new_user.id, action="user_registered", entity_type="User", entity_id=str(new_user.id))
    
    # Generate token
    access_token = create_access_token(data={"sub": new_user.email})
    return {
        "status": "success",
        "data": {"access_token": access_token, "token_type": "bearer", "user": {"id": str(new_user.id), "email": new_user.email}},
        "message": "User registered successfully"
    }

@router.post('/login', response_model=dict)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """Authenticate a user and return a token."""
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.password_hash):
        return {"status": "error", "error_code": "INVALID_CREDENTIALS", "message": "Invalid email or password"}
    
    log_event(db, user.id, action="user_logged_in")
    
    access_token = create_access_token(data={"sub": user.email})
    return {
        "status": "success",
        "data": {"access_token": access_token, "token_type": "bearer"},
        "message": "Login successful"
    }

@router.get('/me', response_model=dict)
def get_me(current_user: User = Depends(get_current_user)):
    """Get the currently authenticated user."""
    return {
        "status": "success",
        "data": {
            "id": str(current_user.id),
            "email": current_user.email,
            "risk_preference": current_user.risk_preference
        },
        "message": "User retrieved"
    }
