from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

        case_sensitive = True
        allow_mutation = False  # Эта настройка делает объект неизменяемым


class DatabaseSettings(Settings):
    HOST: str
    NAME: str
    USER: str
    PASSWORD: str
    PORT: int = Field(default=5432)

    @property
    def postgresql_url(self) -> str:
        return f"postgresql+asyncpg://{self.USER}:{self.PASSWORD}@{self.HOST}:" \
               f"{self.PORT}/{self.NAME}?async_fallback=True"

    class Config:
        env_prefix = "DB_"


class AUTHSettings(Settings):
    JWT_SECRET: str
    USER_MANAGER_SECRET: str

    class Config:
        env_prefix = "AUTH_"


database_settings = DatabaseSettings()
auth_settings = AUTHSettings()
