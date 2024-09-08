from fastapi import HTTPException
from settings import settings
import requests
import os


# Load keys from environment variables or settings
PAYMOB_API_KEY = settings.PAYMOB_API_KEY
PAYMOB_SECRET_KEY = settings.PAYMOB_SECRET_KEY
PAYMOB_PUBLIC_KEY = settings.PAYMOB_PUBLIC_KEY

PAYMOB_API_URL = "https://accept.paymob.com/api"  # Base Paymob URL

# Step 1: Authentication
def get_paymob_token():
    url = f"{PAYMOB_API_URL}/auth/tokens"
    data = {"api_key": PAYMOB_API_KEY}
    
    response = requests.post(url, json=data)
    if response.status_code != 201:
        raise HTTPException(status_code=400, detail="Failed to authenticate with Paymob")
    
    token = response.json().get("token")
    if not token:
        raise HTTPException(status_code=400, detail="No token received from Paymob")
    
    return token

# Step 2: Create an Order
def create_order(token, order_data):
    url = f"{PAYMOB_API_URL}/ecommerce/orders"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(url, json=order_data, headers=headers)
    
    if response.status_code != 201:
        raise HTTPException(status_code=400, detail="Failed to create order with Paymob")
    
    return response.json()

# Define the create_payment function
def create_payment(order_id, amount, currency, return_url):
    token = get_paymob_token()  # Get the token
    payment_data = {
        "amount_cents": amount,
        "currency": currency,
        "payment_method_id": "some_payment_method_id",  # Add appropriate payment method ID
        "order_id": order_id,
        "return_url": return_url
    }
    response = register_payment(token, payment_data)
    return response

# Define the verify_payment function
def verify_payment(payment_token):
    response = handle_payment_confirmation(payment_token)
    return response

# Step 3: Register Payment
def register_payment(token, payment_data):
    url = f"{PAYMOB_API_URL}/acceptance/payment_keys"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(url, json=payment_data, headers=headers)
    
    if response.status_code != 201:
        raise HTTPException(status_code=400, detail="Failed to register payment with Paymob")
    
    return response.json()

# Step 4: Handle Payment Confirmation
def handle_payment_confirmation(payment_token):
    url = f"{PAYMOB_API_URL}/acceptance/payments/pay"
    headers = {"Authorization": f"Bearer {PAYMOB_PUBLIC_KEY}"}
    response = requests.post(url, json={"payment_token": payment_token}, headers=headers)
    
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to confirm payment with Paymob")
    
    return response.json()
