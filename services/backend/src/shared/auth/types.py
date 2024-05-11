from pydantic import BaseModel

class UserInfo(BaseModel):
    at_hash: str
    sub: str
    email_verified: bool
    iss: str
    given_name: str
    nonce: str
    sid: str
    aud: str
    auth_time: int
    name: str
    exp: int
    iat: int
    family_name: str
    email: str