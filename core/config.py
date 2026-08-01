from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str 
    JWT_SECRET_KEY:str = 'test'
    
    model_config = SettingsConfigDict(
        env_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"),
        env_file_encoding='utf-8',
        extra='ignore' 
    )

settings = Settings()
