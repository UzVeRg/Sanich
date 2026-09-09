from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://sanich:sanich@localhost:5432/sanich"

    class Config:
        env_file = ".env"


settings = Settings()