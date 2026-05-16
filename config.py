from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    GEMINI_API_KEY: str = ""
    TAVILY_API_KEY: str = ""

    GITHUB_TOKEN: str = ""
    GITHUB_OWNER: str = ""
    GITHUB_REPO: str = ""

    DISCORD_WEBHOOK_URL: str = ""
    DISCORD_MANAGER_WEBHOOK_URL: str = ""

    REDIS_URL: str = "redis://localhost:6379/0"

    USE_MOCK_AI: bool = False
    

    class Config:
        env_file = ".env"


settings = Settings()