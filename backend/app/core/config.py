from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str
    PROJECT_VERSION: str
    DEBUG: bool
    HOST: str
    PORT: int
    DISEASE_MODEL_PATH: str
    EMBEDDING_MODEL: str
    WHISPER_MODEL: str
    LLM_MODEL: str
    

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()