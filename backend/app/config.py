from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # GitLab configuration
    GITLAB_URL: str = "https://gitlab.com"
    
    # Database configuration
    DATABASE_URL: str = "postgresql://user:password@localhost/dbname"
    
    # Other configuration
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()