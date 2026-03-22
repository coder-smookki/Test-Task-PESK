from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str
    OWM_API_KEY: str = ""
    EXCHANGE_API_KEY: str = ""
    DEBUG: bool = False

    class Config:
        env_file = ".env"


settings = Settings()
