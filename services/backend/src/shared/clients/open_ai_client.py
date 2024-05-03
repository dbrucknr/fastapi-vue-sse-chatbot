# FastAPI Dependencies
from fastapi import Depends

# OpenAI Dependencies
from openai import AsyncOpenAI

# Local Dependencies
from src.settings import get_settings, Settings

def openai_client(settings: Settings = Depends(get_settings)) -> AsyncOpenAI:
    return AsyncOpenAI(
        api_key=settings.openai_api_key,
        organization=settings.openai_api_org
    )