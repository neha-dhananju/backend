from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    APP_NAME: str = "AI Recipe Platform"
    ENV: str = "development"

    SPOONACULAR_API_KEY: str
    FATSECRET_CLIENT_ID: str
    FATSECRET_CLIENT_SECRET: str

    AI_PROVIDER: str = "gemini"
    GEMINI_API_KEY: str | None = None
    OPENAI_API_KEY: str | None = None
    YOUTUBE_API_KEY: str | None = None
    REDIS_URL: str = "redis://localhost:6379"

    HOST: str = "127.0.0.1"
    PORT: int = 8000

    class Config:
        env_file = ".env"


settings = Settings()
