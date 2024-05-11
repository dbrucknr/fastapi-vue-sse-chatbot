# FastAPI Dependencies
from fastapi import Depends

# SQLModel Dependencies
from sqlmodel.ext.asyncio.session import AsyncSession

# Local Dependencies
from src.shared import get_postgres_session, verify_account, Account
from src.modules.conversations import Conversation

###############################################################################
# Create Conversation Handler
# POST: https://dbrucknr.ngrok.io/conversations/create 
###############################################################################
async def create_new_conversation(
    account: Account = Depends(verify_account),
    postgres: AsyncSession = Depends(dependency=get_postgres_session)
) -> Conversation:
    """Create a new default conversation"""
    conversation = Conversation(account_id=account.id)

    postgres.add(instance=conversation)
    await postgres.commit()
    await postgres.refresh(instance=conversation)
    
    return conversation