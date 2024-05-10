import logging
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

log = logging.getLogger("uvicorn")

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    #OpenAI
    openai_api_key: str
    openai_api_org: str
    
    # Auth
    shibboleth_client_id: str = ""
    shibboleth_client_secret: str = ""

    # Local Database
    database_url: str

@lru_cache()
def get_settings() -> BaseSettings:
    log.info("Loading config settings from the environment...")
    return Settings()