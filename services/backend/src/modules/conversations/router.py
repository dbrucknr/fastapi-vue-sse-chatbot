# FastAPI Dependencies
from fastapi import APIRouter

# Local Dependencies
from src.modules.conversations import Conversation
import src.modules.conversations.controllers as controller

conversation_router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"]
)

conversation_router.add_api_route(
    path="/",
    methods=["GET"],
    endpoint=controller.retrieve_all_conversations,
    summary="Retrieve all conversations",
    description="",
    response_model=list[Conversation]
)

conversation_router.add_api_route(
    path="/create",
    methods=["POST"],
    endpoint=controller.create_new_conversation,
    summary="Create new conversations",
    description="",
    response_model=Conversation
)