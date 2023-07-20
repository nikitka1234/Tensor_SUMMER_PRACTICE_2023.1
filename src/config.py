from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

        case_sensitive = True
        allow_mutation = False  # Эта настройка делает объект неизменяемым


class DatabaseSettings(Settings):
    HOST: str = Field(default="postgres")
    NAME: str = Field(default="postgres")
    USER: str = Field(default="postgres")
    PASS: str = Field(default="postgres")
    PORT: int = Field(default=5432)

    @property
    def postgresql_url(self) -> str:
        return f"postgresql+asyncpg://{self.USER}:{self.PASS}@{self.HOST}:" \
               f"{self.PORT}/{self.NAME}?async_fallback=True"

    class Config:
        env_prefix = "DB_"


class TestDatabaseSettings(DatabaseSettings):
    class Config:
        env_prefix = "TEST_DB_"


class AUTHSettings(Settings):
    JWT_SECRET: str = Field(default="SECRET")
    USER_MANAGER_SECRET: str = Field(default="SECRET")

    class Config:
        env_prefix = "AUTH_"


database_settings = DatabaseSettings()
test_database_settings = TestDatabaseSettings()
auth_settings = AUTHSettings()
