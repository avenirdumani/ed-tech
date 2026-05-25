from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

__all__ = ["app_settings"]


class AppSettings(BaseSettings):
    db_url: str = Field(alias="DB_URL")
    secret_key: str = Field(alias="SECRET_KEY")


app_settings = AppSettings()
