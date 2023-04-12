from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Cat Charity Fund'
    app_descr: str = 'Helping cats to live a life'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'secret'

    class Config:
        env_file = '.env'


settings = Settings()
