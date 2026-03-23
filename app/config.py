from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    BOT_TOKEN: str
    OWM_API_KEY: str = ""
    EXCHANGE_API_KEY: str = ""
    DEBUG: bool = False


settings = Settings()
