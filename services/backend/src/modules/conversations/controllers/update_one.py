# FastAPI Dependencies
from fastapi import Depends

# SQLModel Dependencies
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

# Local Dependencies
from src.shared import get_postgres_session
from src.modules.conversations import Conversation

async def update_one_conversation(
    body: Conversation,
    postgres: AsyncSession = Depends(dependency=get_postgres_session)
) -> Conversation:
    # Find the record (Filter on User)
    statement = select(Conversation).where(Conversation.id == conversation.id)
    result = await postgres.exec(statement=statement)
    conversation = result.one()

    # Assign values passed
    conversation = body

    # Refresh the database session and add new values to record
    await postgres.add(instance=conversation)
    await postgres.commit()
    await postgres.refresh(instance=conversation)
    
    return conversation
