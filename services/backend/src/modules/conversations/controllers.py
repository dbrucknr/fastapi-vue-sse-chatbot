# FastAPI Dependencies
from fastapi import Depends

# SQLModel Dependencies
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

# Local Dependencies
from src.shared import get_postgres_session
from .models import Conversation, ConversationCreate

###############################################################################
# Create Conversation Handler
###############################################################################
async def create_new_conversation(
    body: ConversationCreate,
    postgres: AsyncSession = Depends(get_postgres_session)
) -> Conversation:
    # This will need to extract a user ID
    conversation = Conversation(title=body.title, account_id=1)

    postgres.add(instance=conversation)
    await postgres.commit()
    await postgres.refresh(instance=conversation)
    return conversation

###############################################################################
# Retrieve All Conversations Handler
###############################################################################
async def retrieve_all_conversations(
    postgres: AsyncSession = Depends(get_postgres_session)
) -> list[Conversation]:
    # This will need to filter on user -> Extract user from request
    query = select(Conversation)
    result = await postgres.exec(statement=query)
    return [
        Conversation(id=conversation.id, title=conversation.title) 
        for conversation 
        in result
    ]

async def update_one_conversation():
    # Likely for title summarize
    ...

async def remove_one_conversation():
    ...

async def remove_all_conversations():
    ...