from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
import os
from dotenv import load_dotenv

# Prefer .env.local for developer overrides if it exists; fallback to .env
_default_env_file = ".env.local" if os.path.exists(".env.local") else ".env"
load_dotenv(_default_env_file)


class Settings(BaseSettings):
    """Application configuration loaded from environment variables.

    Uses pydantic-settings (Pydantic v2) for environment parsing. Local mode flags allow
    disabling heavier dependencies for quick iteration.
    """

    # Pydantic settings config
    model_config = SettingsConfigDict(env_file=_default_env_file, case_sensitive=True)

    ENV: str = "dev"
    APP_NAME: str = "pr-analyzer"

    # Local mode switches (set LOCAL_MODE=true to enable simplified dependencies)
    LOCAL_MODE: bool = False
    DISABLE_KAFKA: bool = False
    DISABLE_MINIO: bool = False
    DISABLE_EMBEDDING: bool = False

    # GitLab integration
    GITLAB_BASE_URL: AnyHttpUrl | None = "https://gitlab.mycwt.com.cn/MyCWTWebNet/OBT-PC-Code.git"
    GITLAB_TOKEN: Optional[str] = ""

    # Kafka
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    KAFKA_PR_EVENTS_TOPIC: str = "pr_events"
    KAFKA_SUMMARY_TOPIC: str = "pr_summary"

    # PostgreSQL
    PG_HOST: str = "localhost"
    PG_PORT: int = 5432
    PG_DB: str = "pr_analyzer"
    PG_USER: str = "pr_user"
    PG_PASSWORD: str = "pr_password"
    # Optional explicit database URL override (e.g. sqlite:///./data.db). If set, it supersedes PG_* values
    DB_URL: Optional[str] = None

    # MinIO
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_SECURE: bool = False
    MINIO_BUCKET_DIFF: str = "diff-snapshots"

    # Embedding / Model
    EMBEDDING_MODEL_NAME: str = "sentence-transformers/all-MiniLM-L12-v2"
    LLM_PROVIDER: str = "openai"  # or "local"
    OPENAI_API_KEY: Optional[str] = None

    # Observability
    OTEL_EXPORTER_OTLP_ENDPOINT: str = "http://localhost:4318"

    # Misc
    LOG_LEVEL: str = "INFO"


settings = Settings()


def is_local_mode() -> bool:
    return settings.LOCAL_MODE
