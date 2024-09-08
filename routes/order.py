import os
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from bson import ObjectId
from typing import List, Optional
from database import database
from models.order import OrderModel
from schemas.order import OrderCreate, OrderUpdate, OrderOut
from schemas.payment import PaymentCreate
from utils.paymob import create_payment, verify_payment

router = APIRouter()

# Helper function to find an order by ID
async def find_order_by_id(order_id: str):
    order = await database["orders"].find_one({"_id": ObjectId(order_id)})
    if order:
        return OrderModel(**order)

# Admin Routes

# Fetch all orders (Admin only)
@router.get("/admin/orders", response_model=List[OrderOut])
async def get_all_orders():
    orders = await database["orders"].find().to_list(None)
    return [OrderOut(**order) for order in orders]

# Update a specific order (Admin only)
@router.put("/admin/orders/{order_id}")
async def update_order(order_id: str, order_update: OrderUpdate):
    order = await find_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    update_data = order_update.dict(exclude_unset=True)
    result = await database["orders"].update_one({"_id": ObjectId(order_id)}, {"$set": update_data})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Order not found")
    
    updated_order = await find_order_by_id(order_id)
    return OrderOut(**updated_order.dict())

# Delete a specific order (Admin only)
@router.delete("/admin/orders/{order_id}")
async def delete_order(order_id: str):
    result = await database["orders"].delete_one({"_id": ObjectId(order_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Order deleted successfully"}

# User Routes

# Fetch a specific order (Public)
@router.get("/orders/{order_id}", response_model=OrderOut)
async def get_order(order_id: str):
    order = await find_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return OrderOut(**order.dict())

# Create and process payment (User only)
@router.post("/orders/{order_id}/payment")
async def create_payment_for_order(order_id: str, payment_data: PaymentCreate):
    order = await find_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Paymob integration for payment processing
    payment_response = await create_payment(order_id, payment_data)
    
    if payment_response['status'] == 'success':
        return {"message": "Payment processed successfully", "payment_id": payment_response['payment_id']}
    else:
        raise HTTPException(status_code=400, detail="Payment processing failed")

# Verify payment status (User only)
@router.post("/orders/{order_id}/payment/verify")
async def verify_payment_status(order_id: str, payment_id: str):
    order = await find_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Paymob integration to verify payment status
    verification_response = await verify_payment(payment_id)
    
    if verification_response['status'] == 'success':
        # Update order status based on verification
        await database["orders"].update_one({"_id": ObjectId(order_id)}, {"$set": {"payment_status": "paid"}})
        return {"message": "Payment verified successfully"}
    else:
        raise HTTPException(status_code=400, detail="Payment verification failed")
