# Python Dependencies
from typing import AsyncGenerator, Any
from contextlib import asynccontextmanager

# FastAPI Dependencies
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

# Local Dependencies
from src.shared import initialize_postgres
from src.modules.events import event_router
from src.modules.conversations import conversation_router
from src.modules.accounts import account_router
from src.modules import * # SQL Models

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
fastapi.include_router(router=event_router)
fastapi.include_router(router=conversation_router)
fastapi.include_router(router=account_router)

# Root Route
@fastapi.get(path="/", response_model=dict[str, str])
async def root():
    return {
        "status": "ok"
    }