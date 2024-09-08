from pydantic import BaseModel
from typing import Optional

# Schema for product creation
class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    quantity: int
    image_url: Optional[str] = None  # Add this field if you plan to include product images

# Schema for updating product
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    image_url: Optional[str] = None  # Add this field if you plan to include product images

# Schema for retrieving product info
class ProductOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    quantity: int
    image_url: Optional[str] = None  # Add this field if you plan to include product images

    class Config:
        orm_mode = True  # Enable reading data as ORM objects
