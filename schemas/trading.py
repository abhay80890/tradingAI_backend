from pydantic import BaseModel, Field
from typing import Literal, List, Optional
from datetime import datetime

class OrderCreate(BaseModel):
    symbol: str
    side: Literal['buy', 'sell']
    quantity: int = Field(gt=0)
    idempotency_key: str

class OrderResponse(BaseModel):
    id: str
    symbol: str
    side: str
    qty: int
    price: float
    status: str

class PositionResponse(BaseModel):
    id: str
    symbol: str
    quantity: int
    avg_price: float

class PortfolioResponse(BaseModel):
    id: str
    name: str
    cash: float
    positions: List[PositionResponse] = []
