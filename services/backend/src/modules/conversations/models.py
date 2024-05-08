from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, SQLModel

# from src.modules.accounts import Account

# if TYPE_CHECKING:
#     from src.modules.messages import Message

class Conversation(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str | None = Field(default='New Chat')
    account_id: int | None = Field(default=None, foreign_key="account.id")

class ConversationCreate(Conversation):
    """Pydantic data-only model to create new Conversation instances"""
    pass