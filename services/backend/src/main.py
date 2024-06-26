# Python Dependencies
from typing import AsyncGenerator, Any
from contextlib import asynccontextmanager

# FastAPI Dependencies
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

# Local Dependencies
from src.settings import get_settings, Settings
from src.shared import initialize_postgres
from src.modules.events import event_router

# Lifespan Events
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[Any, None]:
    await initialize_postgres()
    yield
    # Can add cleanup methods here

# Application
fastapi = FastAPI(
    title="Server Sent Event (SSE + Redis) Concept",
    summary="Experimental API",
    description="""
        Proof of concept that enables a client to subscribe to the /subscribe endpoint 
        and see real-time updates broadcast when redis is changed.
    """,
    lifespan=lifespan
)

# Middlewares
fastapi.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],  
)

fastapi.add_middleware(
    SessionMiddleware,
    secret_key="some-secret-string"
)

# Module Routes
fastapi.include_router(event_router)

# Root Route
@fastapi.get(path="/", response_model=dict[str, str])
async def root(settings: Settings = Depends(get_settings)):
    return {
        "api_key": settings.openai_api_key,
        "api_org": settings.openai_api_org
    }