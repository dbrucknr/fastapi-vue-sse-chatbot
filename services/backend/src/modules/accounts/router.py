# FastAPI Dependencies
from fastapi import APIRouter

import src.modules.accounts.controllers as controller

account_router = APIRouter(
    prefix="/accounts"
)

account_router.add_api_route(
    path="/login",
    methods=["GET"],
    endpoint=controller.login
)

account_router.add_api_route(
    path="/authenticate",
    methods=["GET"],
    endpoint=controller.authenticate
)