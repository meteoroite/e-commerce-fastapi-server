from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL") 
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

client = AsyncIOMotorClient(DATABASE_URL)
database = client[MONGO_DB_NAME]

# Helper function to convert ObjectId to string
def to_object_id(id: str) -> ObjectId:
    return ObjectId(id)

# Dependency to provide the MongoDB database
async def get_db():
    yield database
