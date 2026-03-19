from pydantic_settings import BaseSettings, SettingsConfigDict

"""
Settings class to load environment variables from .env file. This class uses pydantic to validate the types of the variables and to provide default values if needed. The settings are loaded from the .env file located in the parent directory of the config.py file. The settings can be accessed using the settings variable, which is an instance of the Settings class.
"""

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ALGORITHM: str

    # Forma recomendada para Pydantic v2
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8', extra='ignore')

settings = Settings()