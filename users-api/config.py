from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APPLICATION_VERSION: str
    TEST_MODE: bool
    model_config = SettingsConfigDict(env_file=".env")
    app_version: str = "1.0.0"

    class Config:
        env_file = ".env"