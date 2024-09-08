import os
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Query
from bson import ObjectId
from schemas.product import ProductCreate, ProductUpdate, ProductOut
from schemas.review import ReviewCreate, ReviewUpdate, ReviewOut
from models.product import ProductModel
from models.product import ReviewModel
from database import database
import shutil
from settings import settings

router = APIRouter()

# Helper function to find a product by ID
async def find_product_by_id(product_id: str):
    product = await database["products"].find_one({"_id": ObjectId(product_id)})
    if product:
        return ProductModel(**product)

# Helper function to find a review by ID
async def find_review_by_id(review_id: str):
    review = await database["reviews"].find_one({"_id": ObjectId(review_id)})
    if review:
        return ReviewModel(**review)

# Create a new product
@router.post("/products")
async def create_product(product: ProductCreate):
    new_product = await database["products"].insert_one(product.dict())
    return {"message": "Product created successfully", "product_id": str(new_product.inserted_id)}

# Fetch all products
@router.get("/products")
async def get_products():
    products = await database["products"].find().to_list(None)
    return [ProductOut(**product) for product in products]

# Fetch a specific product
@router.get("/products/{product_id}")
async def get_product(product_id: str):
    product = await find_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return ProductOut(**product.dict())

# Update product data
@router.put("/products/{product_id}")
async def update_product(product_id: str, product_update: ProductUpdate):
    product = await find_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    update_data = product_update.dict(exclude_unset=True)
    if 'images' in update_data:
        # Handle image updates
        image_urls = []
        for image in update_data['images']:
            file_location = os.path.join(settings.FILE_UPLOAD_DIR, image.filename)
            os.makedirs(settings.FILE_UPLOAD_DIR, exist_ok=True)
            with open(file_location, "wb") as f:
                shutil.copyfileobj(image.file, f)
            image_urls.append(f"{settings.BASE_URL}/{file_location}")
        update_data['images'] = image_urls
    
    result = await database["products"].update_one({"_id": ObjectId(product_id)}, {"$set": update_data})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    
    updated_product = await find_product_by_id(product_id)
    return ProductOut(**updated_product.dict())

# Delete a product
@router.delete("/products/{product_id}")
async def delete_product(product_id: str):
    result = await database["products"].delete_one({"_id": ObjectId(product_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}

# Create a review
@router.post("/reviews")
async def create_review(review: ReviewCreate):
    new_review = await database["reviews"].insert_one(review.dict())
    return {"message": "Review created successfully", "review_id": str(new_review.inserted_id)}

# Fetch all reviews for a product
@router.get("/reviews/{product_id}")
async def get_reviews(product_id: str):
    reviews = await database["reviews"].find({"product_id": ObjectId(product_id)}).to_list(None)
    return [ReviewOut(**review) for review in reviews]

# Fetch a specific review
@router.get("/reviews/review/{review_id}")
async def get_review(review_id: str):
    review = await find_review_by_id(review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return ReviewOut(**review.dict())

# Update a review
@router.put("/reviews/{review_id}")
async def update_review(review_id: str, review_update: ReviewUpdate):
    review = await find_review_by_id(review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    update_data = review_update.dict(exclude_unset=True)
    result = await database["reviews"].update_one({"_id": ObjectId(review_id)}, {"$set": update_data})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Review not found")
    
    updated_review = await find_review_by_id(review_id)
    return ReviewOut(**updated_review.dict())

# Delete a review
@router.delete("/reviews/{review_id}")
async def delete_review(review_id: str):
    result = await database["reviews"].delete_one({"_id": ObjectId(review_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Review not found")
    return {"message": "Review deleted successfully"}
