from fastapi import FastAPI
from .api.routes import router
from .core.config import settings
from .core.db import engine
from .models import Base

app = FastAPI(title=settings.APP_NAME)

@app.on_event("startup")
def startup_event():
    # Ensure tables exist (SQLite local mode convenience; in prod use migrations)
    Base.metadata.create_all(bind=engine)
app.include_router(router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "PR Analyzer Backend", "env": settings.ENV}
