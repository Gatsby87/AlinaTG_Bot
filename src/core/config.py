import os
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """Настройки приложения"""
    
    # Telegram
    TELEGRAM_TOKEN: str
    
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./alina.db"
    
    # YooKassa
    YOOKASSA_SHOP_ID: str
    YOOKASSA_API_KEY: str
    YOOKASSA_WEBHOOK_URL: str
    SUBSCRIPTION_PRICE: float = 299.0
    
    # DeepSeek AI
    DEEPSEEK_API_KEY: str
    DEEPSEEK_API_URL: str = "https://api.deepseek.com/v1/chat/completions"
    
    # Web Admin
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 30
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WEBHOOK_HOST: str
    
    # Bot Settings
    TRIAL_DAYS: int = 1
    MAX_MESSAGES_PER_MINUTE: int = 10
    MAX_HISTORY_LENGTH: int = 10
    
    class Config:
        env_file = ".env"

settings = Settings()