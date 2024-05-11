# FastAPI Dependencies
from fastapi import APIRouter

import src.shared.auth.controllers as controller

auth_router = APIRouter(
    prefix="/auth"
)

auth_router.add_api_route(
    path="/login",
    methods=["GET"],
    endpoint=controller.login
)

auth_router.add_api_route(
    path="/authenticate",
    methods=["GET"],
    endpoint=controller.authenticate
)