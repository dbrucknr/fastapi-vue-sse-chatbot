# Python Dependencies
from typing import AsyncGenerator, Any
from contextlib import asynccontextmanager

# FastAPI Dependencies
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

# Local Dependencies
from src.shared import initialize_postgres, auth_router, verify_account

from src.modules.events import event_router
from src.modules.conversations import conversation_router

# SQL Models
from src.modules import *
from src.shared.auth.models import *

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
fastapi.include_router(router=auth_router)

# Root Route
@fastapi.get(path="/", response_model=dict[str, str])
async def root(
    account: Account = Depends(verify_account)
):
    print(account)
    return {
        "status": "ok"
    }