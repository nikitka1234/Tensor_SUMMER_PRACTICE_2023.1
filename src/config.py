from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

        case_sensitive = True
        allow_mutation = False  # Эта настройка делает объект неизменяемым.


class DatabaseSettings(Settings):
    host: str
    name: str
    user: str
    password: str
    port: int = Field(default=5432)

    @property
    def postgresql_url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

    class Config:
        env_prefix = "DB_"


database_settings = DatabaseSettings()
