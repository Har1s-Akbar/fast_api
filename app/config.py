from pydantic import BaseSettings

class Settings(BaseSettings):
    secret_key: str
    algorith:str
    database:str
    username:str
    password:str
    host:str
    database_name:str
    access_token_expire_minutes: int
    
    class Config:
        case_sensitive = True
        env_file= '../.env'
        env_file_coding = 'utf-8'

settings = Settings()