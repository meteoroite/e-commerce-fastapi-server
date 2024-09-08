from pydantic import BaseModel, EmailStr
from bson import ObjectId
from typing import Optional

class UserModel(BaseModel):
    id: Optional[str] = None  # MongoDB uses ObjectId
    username: str
    email: EmailStr
    hashed_password: str
    is_active: bool = False
    email_verified: bool = False
    is_admin: bool = False
    profile_image: Optional[str] = None  # Add this if you plan to include profile images

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
