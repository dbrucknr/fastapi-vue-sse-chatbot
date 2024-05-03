from sqlmodel import SQLModel, Field

# One account can have many conversations
class Account(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

    