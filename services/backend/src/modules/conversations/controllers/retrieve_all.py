# FastAPI Dependencies
from fastapi import Depends

# SQLModel Dependencies
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

# Local Dependencies
from src.shared import get_postgres_session
from src.modules.conversations import Conversation

###############################################################################
# Retrieve All Conversations Handler
# GET: https://dbrucknr.ngrok.io/conversations/
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