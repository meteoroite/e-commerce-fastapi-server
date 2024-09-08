import os
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from datetime import timedelta
from utils.auth import register_new_user, login_for_access_token, send_password_reset_email, verify_password, create_access_token, get_current_user
from schemas.auth import UserCreate, UserLogin, PasswordResetRequest, SetNewPassword, EmailVerification
from schemas.user import UserUpdate, UserOut
from models.user import UserModel
from database import database
from bson import ObjectId
import shutil
from settings import settings

router = APIRouter()

# Helper function to find user by email
async def find_user_by_email(email: str):
    user = await database["users"].find_one({"email": email})
    if user:
        return UserModel(**user)

# Helper function to find user by ID
async def find_user_by_id(user_id: str):
    user = await database["users"].find_one({"_id": ObjectId(user_id)})
    if user:
        return UserModel(**user)

# Register new user
@router.post("/register")
async def register(user: UserCreate):
    existing_user = await find_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = await register_new_user(user)
    return {"message": "User registered successfully"}

# Email verification
@router.post("/verify-email")
async def verify_email(verification: EmailVerification):
    user = await find_user_by_email(verification.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Logic to verify email with token (e.g., set `email_verified` to True)
    # For simplicity, assume verification is successful
    await database["users"].update_one({"email": verification.email}, {"$set": {"email_verified": True}})
    return {"message": "Email verified successfully"}

# Activate user account
@router.post("/activate/{user_id}")
async def activate_account(user_id: str):
    user = await find_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    await database["users"].update_one({"_id": ObjectId(user_id)}, {"$set": {"is_active": True}})
    return {"message": "Account activated successfully"}

# User login
@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await find_user_by_email(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"sub": str(user.id)}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

# Password reset request
@router.post("/password-reset")
async def password_reset(request: PasswordResetRequest):
    user = await find_user_by_email(request.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    await send_password_reset_email(request.email, database)
    return {"message": "Password reset email sent"}

# Set new password
@router.post("/set-new-password")
async def set_new_password(password_data: SetNewPassword):
    if password_data.new_password != password_data.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    # Logic to update password goes here
    # For example, you might need to verify the reset token and update the password in the database
    return {"message": "Password updated successfully"}

# Update user profile
@router.put("/update/{user_id}")
async def update_user(user_id: str, user_update: UserUpdate, current_user=Depends(get_current_user)):
    if str(current_user.id) != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this user")

    update_data = user_update.dict(exclude_unset=True)
    if 'password' in update_data:
        update_data['hashed_password'] = create_access_token(update_data['password'])
        del update_data['password']
    
    result = await database["users"].update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    
    updated_user = await find_user_by_id(user_id)
    return UserOut(**updated_user.dict())

# Delete user account
@router.delete("/delete/{user_id}")
async def delete_user(user_id: str, current_user=Depends(get_current_user)):
    if str(current_user.id) != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this user")

    result = await database["users"].delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"message": "User deleted successfully"}

# Update profile image
@router.post("/update-profile-image/{user_id}")
async def update_profile_image(user_id: str, file: UploadFile = File(...), current_user=Depends(get_current_user)):
    if str(current_user.id) != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this user")

    file_location = os.path.join(settings.FILE_UPLOAD_DIR, file.filename)
    os.makedirs(settings.FILE_UPLOAD_DIR, exist_ok=True)
    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)
    
    # Update user profile with image URL
    image_url = f"{settings.BASE_URL}/{file_location}"
    await database["users"].update_one({"_id": ObjectId(user_id)}, {"$set": {"profile_image": image_url}})
    
    return {"message": "Profile image updated successfully", "image_url": image_url}
