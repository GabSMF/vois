"""
Application settings and configuration
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # API Configuration
    api_v1_prefix: str = "/api/v1"
    debug: bool = False
    title: str = "Vois Capture API Gateway"
    description: str = "Database-agnostic API gateway for multimedia capture processing"
    version: str = "1.0.0"

    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000

    # File Upload Configuration
    max_upload_size: int = 100 * 1024 * 1024  # 100MB
    allowed_audio_types: list = ["audio/mpeg", "audio/wav", "audio/mp3", "audio/m4a"]
    allowed_image_types: list = ["image/jpeg", "image/png", "image/gif", "image/webp"]

    # CORS Configuration
    cors_origins: list = ["http://localhost:3000", "http://localhost:8080"]
    cors_allow_credentials: bool = True
    cors_allow_methods: list = ["*"]
    cors_allow_headers: list = ["*"]

    # Upload Directory
    upload_dir: str = "./uploads"

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()