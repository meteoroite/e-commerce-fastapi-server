from pydantic import BaseModel, Field, PositiveFloat, constr
from typing import Optional, Dict, List

class PaymentCreate(BaseModel):
    amount: PositiveFloat = Field(..., description="Amount to be paid in the smallest currency unit (e.g., cents for USD)")
    currency: str = Field(..., min_length=3, max_length=3, description="Currency code (e.g., 'USD', 'EGP')")  # Define min/max length in Field
    description: Optional[str] = Field(None, description="Description of the payment (e.g., 'Payment for order #12345')")
    order_id: Optional[str] = Field(None, description="ID of the related order")
    customer_email: Optional[str] = Field(None, description="Email of the customer making the payment")
    customer_phone: Optional[str] = Field(None, description="Phone number of the customer")
    payment_method: Optional[str] = Field(None, description="Payment method (e.g., 'card', 'wallet')")
    metadata: Optional[Dict[str, str]] = Field(None, description="Additional metadata for the payment")

    integration_id: Optional[str] = Field(None, description="Integration ID for the payment provider")
    items: Optional[List[Dict[str, str]]] = Field(None, description="List of items in the order")

class PaymentStatus(BaseModel):
    status: str = Field(..., description="Payment status (e.g., 'success', 'failed', 'pending')")
    payment_id: Optional[str] = Field(None, description="ID of the payment transaction")
    order_id: Optional[str] = Field(None, description="ID of the related order")
    amount_paid: Optional[PositiveFloat] = Field(None, description="Amount that was successfully paid")
    currency: str = Field(..., min_length=3, max_length=3, description="Currency code (e.g., 'USD')")  # Define min/max length in Field
    created_at: Optional[str] = Field(None, description="Timestamp when the payment was created")
    paid_at: Optional[str] = Field(None, description="Timestamp when the payment was completed")
    transaction_details: Optional[Dict[str, str]] = Field(None, description="Details of the transaction (e.g., card last 4 digits, payment gateway response)")

    failure_reason: Optional[str] = Field(None, description="Reason for payment failure if applicable")
