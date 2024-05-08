from fastapi import APIRouter
import src.modules.conversations.controllers as controller

conversation_router = APIRouter()

conversation_router.add_api_route(
    path="/conversations",
    methods=["GET"],
    endpoint=controller.retrieve_all_conversations,
    summary="Retrieve all conversations",
    description=""
)