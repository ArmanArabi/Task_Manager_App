from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str 
    JWT_SECRET_KEY:str = 'test'
    CELERY_BROKER_URL:str = 'redis://redis:6379/3', #redis://localhost<service name>:port/database number 
    CELERY_BACKEND_URL:str = 'redis://redis:6379/3'
    
    model_config = SettingsConfigDict(
        env_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"),
        env_file_encoding='utf-8',
        extra='ignore' 
    )

settings = Settings()
