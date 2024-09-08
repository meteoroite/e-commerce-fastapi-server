from pydantic import BaseModel, EmailStr
from typing import Optional

# Token schema for JWT token response
class Token(BaseModel):
    access_token: str
    token_type: str

# Token data for extracting user info from the token
class TokenData(BaseModel):
    id: Optional[str] = None

# User schema for creating new users
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

# User schema for login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Schema for password reset request
class PasswordResetRequest(BaseModel):
    email: EmailStr

# Schema for setting a new password
class SetNewPassword(BaseModel):
    new_password: str
    confirm_password: str

# Schema for email verification token
class EmailVerification(BaseModel):
    email: str
    token: str