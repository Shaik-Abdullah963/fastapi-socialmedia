from pydantic_settings import BaseSettings
from pydantic import Field
from pathlib import Path

class Settings(BaseSettings):
    database_hostname: str 
    database_port: str 
    database_password: str
    database_name: str 
    database_username: str 
    secret_key: str 
    algorithm: str 
    access_token_expire_minutes: int 
    
    class Config:
        env_file = str(Path(__file__).parent.parent / ".env")

settings = Settings()