E-commerce API
Overview
This repository contains the server code for an E-commerce API built with FastAPI. The API provides routes for managing users, products, orders, and carts. It uses MongoDB as the database and integrates with the Paymob payment gateway.

Project Structure
main.py: Entry point for the FastAPI application.
database.py: Contains the MongoDB client setup and database dependency.
routes/: Contains route definitions for various resources (user, product, order, cart).
schemas/: Contains Pydantic models for request and response validation.
models/: Contains Pydantic models for MongoDB documents.
utils/: Contains utility functions, such as Paymob payment integration.
Installation
Clone the Repository:

bash
Copy code
git clone https://github.com/your-username/your-repository.git
cd your-repository
Create a Virtual Environment:

bash
Copy code
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install Dependencies:

bash
Copy code
pip install -r requirements.txt
Create a .env File:

Copy the .env.example file to .env and update it with your environment-specific values.

Run the Server:

bash
Copy code
uvicorn main:app --reload
Routes
User Routes
POST /users/: Create a new user.
GET /users/{user_id}: Retrieve a user by ID.
PUT /users/{user_id}: Update a user by ID.
DELETE /users/{user_id}: Delete a user by ID.
Product Routes
POST /products/: Create a new product.
GET /products/{product_id}: Retrieve a product by ID.
PUT /products/{product_id}: Update a product by ID.
DELETE /products/{product_id}: Delete a product by ID.
Order Routes
POST /orders/: Create a new order.
GET /orders/{order_id}: Retrieve an order by ID.
PUT /orders/{order_id}: Update an order by ID.
DELETE /orders/{order_id}: Delete an order by ID.
Cart Routes
POST /carts/: Create a new cart.
GET /carts/{cart_id}: Retrieve a cart by ID.
PUT /carts/{cart_id}: Update a cart by ID.
DELETE /carts/{cart_id}: Delete a cart by ID.
Schemas
User
UserCreate: Schema for creating a new user.
UserUpdate: Schema for updating an existing user.
UserOut: Schema for returning user data.
Product
ProductCreate: Schema for creating a new product.
ProductUpdate: Schema for updating an existing product.
ProductOut: Schema for returning product data.
Order
OrderCreate: Schema for creating a new order.
OrderUpdate: Schema for updating an existing order.
OrderOut: Schema for returning order data.
Cart
CartCreate: Schema for creating a new cart.
CartUpdate: Schema for updating an existing cart.
CartOut: Schema for returning cart data.
Review
ReviewCreate: Schema for creating a new review.
ReviewUpdate: Schema for updating an existing review.
ReviewOut: Schema for returning review data.
Models
ReviewModel
id: Optional, MongoDB ObjectId.
user_id: User ID.
rating: Rating given by the user.
comment: Optional, review comment.
created_at: Optional, review creation timestamp.
ProductModel
id: Optional, MongoDB ObjectId.
name: Product name.
description: Optional, product description.
price: Product price.
quantity: Quantity available.
image_url: Optional, URL to product image.
reviews: Optional, list of reviews for the product.
Middleware
Paymob Integration
get_paymob_token: Authenticates with Paymob and retrieves an API token.
create_order: Creates an order with Paymob.
register_payment: Registers a payment with Paymob.
handle_payment_confirmation: Confirms payment with Paymob.
Usage
Starting the Server:

Run the server with uvicorn:

bash
Copy code
uvicorn main:app --reload
Access the API:

The server will be accessible at http://localhost:8000. You can interact with the API using tools like Postman or cURL.

Authentication:

Authentication is managed through JWT tokens. Ensure you set the appropriate environment variables for the JWT settings.

Payment Integration:

Ensure the Paymob credentials are correctly set in the .env file for payment processing.

Contributing
Feel free to open issues or submit pull requests to improve the project. Please follow the code of conduct and contributing guidelines provided.

License
This project is licensed under the MIT License - see the LICENSE file for details.

