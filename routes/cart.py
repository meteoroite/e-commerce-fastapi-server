from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from database import database
from models.product import ProductModel as products
from utils.auth import get_current_user

router = APIRouter()

# In-memory cart for simplicity
cart = {}

class CartItem(BaseModel):
    product_id: int
    quantity: int

@router.post("/cart/add")
async def add_to_cart(item: CartItem, current_user: dict = Depends(get_current_user)):
    # Check if product exists
    query = products.select().where(products.c.id == item.product_id)
    product = await database.fetch_one(query)
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Add product to cart for the current user
    user_cart = cart.get(current_user["id"], [])
    
    # Check if product is already in the cart, if so update quantity
    for cart_item in user_cart:
        if cart_item["product_id"] == item.product_id:
            cart_item["quantity"] += item.quantity
            break
    else:
        # Add a new product to the cart
        user_cart.append({"product_id": item.product_id, "quantity": item.quantity})
    
    cart[current_user["id"]] = user_cart
    
    return {"message": "Item added to cart"}

@router.get("/cart/")
async def view_cart(current_user: dict = Depends(get_current_user)):
    # Fetch cart for the current user
    user_cart = cart.get(current_user["id"], [])
    
    if not user_cart:
        return {"message": "Your cart is empty"}
    
    # Fetch product details for items in the cart
    cart_details = []
    for item in user_cart:
        query = products.select().where(products.c.id == item["product_id"])
        product = await database.fetch_one(query)
        cart_details.append({
            "product": product,
            "quantity": item["quantity"]
        })
    
    return {"cart": cart_details}

@router.delete("/cart/remove/{product_id}")
async def remove_from_cart(product_id: int, current_user: dict = Depends(get_current_user)):
    user_cart = cart.get(current_user["id"], [])
    
    # Remove the item from the cart
    for cart_item in user_cart:
        if cart_item["product_id"] == product_id:
            user_cart.remove(cart_item)
            cart[current_user["id"]] = user_cart
            return {"message": "Item removed from cart"}
    
    raise HTTPException(status_code=404, detail="Item not found in cart")
