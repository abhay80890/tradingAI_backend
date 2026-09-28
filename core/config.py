from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    """
    This class loads all the variables from the .env file.
    By using Pydantic, it automatically checks if the variables are 
    the right type (e.g., ensuring ACCESS_TOKEN_EXPIRE_MINUTES is an integer).
    """
    
    # Project Info
    PROJECT_NAME: str = "FinPilot AI API"

    # API Keys (Optional here just in case they aren't filled in yet, so the app doesn't crash on boot)
    ALPHA_VANTAGE_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    NVIDIA_API_KEY: Optional[str] = None

    # Database URLs
    DATABASE_URL: str
    REDIS_URL: str
    QDRANT_HOST: str
    QDRANT_PORT: int

    # Security Config
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # This tells Pydantic where to look for the variables
    model_config = SettingsConfigDict(env_file="../.env", env_file_encoding="utf-8")

# Create a single instance of the settings to be imported and used in other files
settings = Settings()
