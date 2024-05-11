from typing import Optional
from sqlmodel import SQLModel, Field

# One account can have many conversations
class Account(SQLModel, table=True):
    """
    Provides the primary Postgres Table instance.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    given_name: str
    family_name: str
    email: str
    email_verified: bool = Field(default=False)
    # refresh_token: Optional[str]


class AccountCreate(SQLModel):
    """
    Minimum attributes required to create an Account Instance
    """
    name: str
    given_name: str
    family_name: str
    email: str
    email_verified: str


class AccountRead(SQLModel):
    """Attributes to be sent as a response. Hides unnecessary"""

    id: int
    name: str
    given_name: str
    family_name: str
    email: str


class AccountUpdate(SQLModel):
    """Minimum attributes required on PATCH requests"""

    name: str
    given_name: str
    family_name: str
    email: str
    # refresh_token: str

    