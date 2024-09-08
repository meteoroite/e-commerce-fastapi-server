from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Schema for creating an order
class OrderCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int

# Schema for updating an order
class OrderUpdate(BaseModel):
    status: Optional[str] = None
    quantity: Optional[int] = None

# Schema for retrieving order info
class OrderOut(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int
    total_price: float
    status: str
    created_at: datetime

    class Config:
        orm_mode = True
