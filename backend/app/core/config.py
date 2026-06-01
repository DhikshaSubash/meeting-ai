from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    APP_NAME: str = "Meeting AI"
    DEBUG: bool = True
    VERSION: str = "0.1.0"

    SECRET_KEY: str = "change-this-in-production"
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/meetingai"

    UPLOAD_DIR: Path = Path("../uploads")   # ← back to this
    MODELS_DIR: Path = Path("../models")

    HF_TOKEN: str = ""

    class Config:
        env_file = ".env"

settings = Settings()