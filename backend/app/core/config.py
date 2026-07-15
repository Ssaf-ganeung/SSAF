from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"
    DATABASE_URL: str = "sqlite:///./app.db"
    CORS_ORIGINS: str = "http://localhost:5173"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]


settings = Settings()
