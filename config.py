from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env'
    )

    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    BOT_TOKEN: SecretStr
    SUPER_ADMIN_ID: int

    WEBHOOK_HOST: str
    WEBHOOK_SECRET: str

    WEBAPP_HOST: str = '0.0.0.0'
    WEBAPP_PORT: int = 3000

    def get_db_url(self) -> str:
        return (f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@"
                f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")

    def get_alembic_url(self) -> str:
        return (f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@"
                f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")

    def get_webhook_path(self) -> str:
        return f'/webhook/{self.BOT_TOKEN.get_secret_value()}'

    def get_webhook_url(self) -> str:
        return f'{self.WEBHOOK_HOST}{self.get_webhook_path()}'


settings = Settings()
