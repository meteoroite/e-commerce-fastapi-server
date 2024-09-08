from fastapi import FastAPI
from routes import user, product, order, cart
from database import database
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    print("Database connected")
    
    yield  # The application runs here
    
    # Shutdown logic
    print("Database disconnected")

# Initialize FastAPI app with lifespan context
app = FastAPI(lifespan=lifespan)

# Include routers
app.include_router(user.router)
app.include_router(product.router)
app.include_router(order.router)
app.include_router(cart.router)
