from pydantic_settings import BaseSettings
from typing import List, Union
import os
import json

def get_cors_origins() -> List[str]:
    """Get CORS origins from environment or use defaults"""
    env_origins = os.getenv("BACKEND_CORS_ORIGINS")
    if env_origins:
        try:
            return json.loads(env_origins)
        except json.JSONDecodeError:
            # Handle comma-separated string
            return [origin.strip() for origin in env_origins.split(",")]
    return [
        "http://localhost:3000", "http://localhost:3001", "http://localhost:3002",
        "http://localhost:3003", "http://localhost:3004", "http://localhost:3005",
        "http://localhost:3006", "http://localhost:8000", "http://127.0.0.1:8000",
        # Production URLs - GitHub Pages
        "https://muzamil-ai-dev.github.io",
        # Hugging Face Spaces
        "https://huggingface.co",
        "https://*.hf.space",
        "https://muzamil-ai-dev-todo-backend.hf.space",
    ]

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    """
    # Backend configuration
    BACKEND_CORS_ORIGINS: List[str] = get_cors_origins()
    BACKEND_PORT: int = 8000
    BACKEND_HOST: str = "localhost"

    # Database configuration
    DATABASE_URL: str
    TEST_DATABASE_URL: str = ""

    # JWT configuration
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Better Auth configuration
    BETTER_AUTH_SECRET: str
    BETTER_AUTH_TRUST_HOST: bool = True

    # Application configuration
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    SERVER_NAME: str = "localhost"
    SERVER_HOST: str = "http://localhost:8000"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()