from typing import TYPE_CHECKING, Optional
from sqlmodel import SQLModel, Field, Relationship

from src.modules.conversations import Conversation
# if TYPE_CHECKING:
#     from src.modules.conversations import Conversation

class Message(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    query: str
    response: str
    conversation_id: Optional[int] = Field(default=None, foreign_key="conversation.id")
    # conversation: Optional[Conversation] = Relationship(back_populates="conversations")