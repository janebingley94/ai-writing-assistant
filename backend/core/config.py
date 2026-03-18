from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: Optional[str] = None
    openai_base_url: Optional[str] = None
    default_model: str = "gpt-4o-mini"

    database_url: Optional[str] = None
    db_host: str = "localhost"
    db_port: int = 5432
    db_user: str = "postgres"
    db_password: str = "postgres"
    db_name: str = "ai_writing_assistant"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    def model_post_init(self, __context) -> None:
        if not self.database_url:
            self.database_url = (
                "postgresql+asyncpg://"
                f"{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
            )


settings = Settings()
