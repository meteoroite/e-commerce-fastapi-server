from pydantic import BaseModel
from bson import ObjectId
from typing import Optional, List

# Define the Review model if not already defined
class ReviewModel(BaseModel):
    id: Optional[str] = None  # MongoDB uses ObjectId
    user_id: str
    rating: int
    comment: Optional[str] = None
    created_at: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }

class ProductModel(BaseModel):
    id: Optional[str] = None  # MongoDB uses ObjectId
    name: str
    description: Optional[str]
    price: float
    quantity: int
    image_url: Optional[str] = None
    reviews: Optional[List[ReviewModel]] = None  # Add this field to include reviews

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
