"""Configuration management"""

from pydantic_settings import BaseSettings
from typing import Literal


class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    google_api_key: str
    gemini_model: str = "gemini-flash-latest"  # ← PUT YOUR WORKING MODEL HERE
    
    # App Configuration
    tiktok_mock_mode: bool = True
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()