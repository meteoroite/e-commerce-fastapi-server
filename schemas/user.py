from pydantic import BaseModel, EmailStr
from typing import Optional

# Base user schema (for internal use)
class UserBase(BaseModel):
    username: str
    email: EmailStr
    is_active: bool = False
    email_verified: bool = False
    is_admin: bool = False
    profile_image: Optional[str] = None  # Add this if you plan to include profile images

# Schema for creating a user
class UserCreate(UserBase):
    password: str

# Schema for updating a user
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    email_verified: Optional[bool] = None
    is_admin: Optional[bool] = None
    profile_image: Optional[str] = None

# Schema for displaying user info
class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True  # Enable reading data as ORM objects
