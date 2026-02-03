"""Configuration management"""

from pydantic_settings import BaseSettings
from typing import Literal


class Settings(BaseSettings):
    """Application settings with TikTok API support"""
    
    # Gemini LLM
    google_api_key: str
    gemini_model: str = "gemini-flash-latest"
    
    # TikTok Marketing API
    tiktok_app_id: str = ""
    tiktok_app_secret: str = ""
    tiktok_access_token: str = ""
    tiktok_advertiser_id: str = ""
    tiktok_mock_mode: bool = True  # Set to False when you have real credentials
    
    # Application
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()