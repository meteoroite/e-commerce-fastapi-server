from pydantic import BaseModel
from bson import ObjectId
from typing import Optional

class ReviewBase(BaseModel):
    user_id: str
    product_id: str
    rating: int
    comment: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }

class ReviewCreate(ReviewBase):
    pass

class ReviewUpdate(ReviewBase):
    rating: Optional[int] = None
    comment: Optional[str] = None

class ReviewOut(ReviewBase):
    id: str
    created_at: Optional[str] = None
