# FastAPI Dependencies
from fastapi import Depends

# HTTP Dependencies
from httpx import AsyncClient, Limits

# OpenAI Dependencies
from openai import AsyncOpenAI

# Local Dependencies
from src.settings import get_settings, Settings

###############################################################################
# OpenAI Client
###############################################################################
def openai_client(
    settings: Settings = Depends(get_settings)
) -> AsyncOpenAI:
    return AsyncOpenAI(
        api_key=settings.openai_api_key,
        organization=settings.openai_api_org,
        http_client=AsyncClient(
            limits=Limits(
                max_connections=1000,
                max_keepalive_connections=100
            )
        )
    )