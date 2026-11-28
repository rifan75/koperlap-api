from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    APP_NAME: str = "Koperasi API"
    APP_VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"

    DATABASE_URL: str
    # JWT_SECRET_KEY: str karena kita menggunakan RSA, kita tidak memerlukan secret key lagi
    JWT_ALGORITHM: str = "RS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    JWT_PRIVATE_KEY_PATH: Path = Path(
        "secrets/jwt-private.pem"
    )

    JWT_PUBLIC_KEY_PATH: Path = Path(
        "secrets/jwt-public.pem"
    )

    JWT_ISSUER: str = "koperlap-api"
    JWT_AUDIENCE: str = "koperasi-api-users"

    REDIS_URL: str = "redis://localhost:6379/0"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()