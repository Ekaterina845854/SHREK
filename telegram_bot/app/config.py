from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    BOT_TOKEN: str
    
    REDIS_HOST: str
    REDIS_PORT: int
    
    API_BASE_URL: str
    
    CACHE_TTL: int
    
    model_config = SettingsConfigDict(
        env_file=".bot.env",
    )
    
    @property
    def SQLALCHEMY_DATABASE_URL(self):
        return (f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@"
                f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")


config = Config()
