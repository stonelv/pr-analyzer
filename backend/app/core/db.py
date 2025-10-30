from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import settings, is_local_mode
import os

if settings.DB_URL:
    DATABASE_URL = settings.DB_URL
elif is_local_mode():
    # use sqlite file for local dev without docker
    os.makedirs("data", exist_ok=True)
    DATABASE_URL = "sqlite:///./data/local.db"
else:
    # Use psycopg (v3) driver name; requirements (full) include psycopg[binary]
    DATABASE_URL = f"postgresql+psycopg://{settings.PG_USER}:{settings.PG_PASSWORD}@{settings.PG_HOST}:{settings.PG_PORT}/{settings.PG_DB}"

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, pool_pre_ping=True, future=True, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
