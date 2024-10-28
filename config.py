from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    HOST_IP: str = Field()
    REDIS_PORT: str = Field()
    REDIS_HOST: str = Field()
    BOT_IP: str = Field()
    OPENAI_API_KEY: str = Field()


settings = Settings()
