from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "DClaw Offboard"
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/dclaw_offboard"
    cors_origins: str = "*"

    class Config:
        env_prefix = "OFFBOARD_"

settings = Settings()
