from pydantic import BaseModel
from typing import Optional
from bson import ObjectId

class OrderModel(BaseModel):
    id: Optional[str] = None  # MongoDB uses ObjectId
    user_id: str
    product_id: str
    quantity: int
    total_price: float
    status: str = "pending"
    created_at: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
