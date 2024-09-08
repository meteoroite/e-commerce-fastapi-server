import os
from pydantic_settings import BaseSettings
from typing import Optional

def str_to_bool(value: str) -> bool:
    return value.lower() in ("true", "1", "yes")

class Settings(BaseSettings):
    # Application Settings
    APP_NAME: str = "E-commerce API"
    APP_VERSION: str = "1.0.0"
    BASE_URL: str = os.getenv("BASE_URL", "http://localhost:8000")

    # Database Settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
    MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME", "ecommerce_db")
    
    # Security and JWT Settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

    # Email Settings for verification and password reset
    EMAIL_USERNAME: str = os.getenv("EMAIL_USERNAME", "your-email@example.com")
    EMAIL_PASSWORD: str = os.getenv("EMAIL_PASSWORD", "your-email-password")
    EMAIL_FROM: str = os.getenv("EMAIL_FROM", "no-reply@example.com")
    EMAIL_PORT: int = int(os.getenv("EMAIL_PORT", 587))
    EMAIL_SERVER: str = os.getenv("EMAIL_SERVER", "smtp.gmail.com")
    EMAIL_USE_TLS: bool = str_to_bool(os.getenv("EMAIL_USE_TLS", "true"))
    EMAIL_USE_SSL: bool = str_to_bool(os.getenv("EMAIL_USE_SSL", "false"))

    # Paymob API Settings
    PAYMOB_API_KEY: str = os.getenv("PAYMOB_API_KEY", "")
    PAYMOB_SECRET_KEY: str = os.getenv("PAYMOB_SECRET_KEY", "")
    PAYMOB_PUBLIC_KEY: str  = os.getenv("PAYMOB_PUBLIC_KEY", "")

    # Debug Setting
    DEBUG: bool = str_to_bool(os.getenv("DEBUG", "false"))

    class Config:
        env_file = ".env"  # Load environment variables from .env file
        case_sensitive = True  # Make environment variable names case-sensitive

# Create an instance of the settings
settings = Settings()
