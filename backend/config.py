from pydantic_settings import BaseSettings

"""
Settings class to load environment variables from .env file. This class uses pydantic to validate the types of the variables and to provide default values if needed. The settings are loaded from the .env file located in the parent directory of the config.py file. The settings can be accessed using the settings variable, which is an instance of the Settings class.
"""

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = "../.env"

settings = Settings()