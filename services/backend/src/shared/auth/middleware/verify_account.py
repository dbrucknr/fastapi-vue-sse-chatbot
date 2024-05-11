from datetime import datetime
from fastapi import Request, HTTPException, Depends

# SQLModel Dependencies
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from authlib.jose import jwt, JWTClaims

from src.settings import get_settings, Settings
from src.shared import get_postgres_session
from src.shared.auth.shibboleth import shibboleth
from src.shared.auth.models import Account

def get_id_token(request: Request) -> str:
    """Extract ID Token from Request Session"""
    id_token: str = request.session.get("id_token")

    if id_token is None:
        raise HTTPException(status_code=401, detail="Unauthenticated. Access Denied.")
    
    return id_token

async def get_userinfo(
    id_token: str = Depends(get_id_token),
) -> JWTClaims:
    """Extract UserInfo from the ID Token"""
    jwks = await shibboleth.fetch_jwk_set()
    userinfo: JWTClaims = jwt.decode(s=id_token, key=jwks)

    return userinfo

async def verify_userinfo(
    userinfo: JWTClaims = Depends(get_userinfo),
    settings: Settings = Depends(get_settings)
) -> str:
    """Compare extracted userinfo with OIDC server metadata. Returns the user email"""
    metadata = await shibboleth.load_server_metadata()

    if userinfo["iss"] != metadata["issuer"]:
        raise HTTPException(status_code=401, detail="Unauthenticated. Access Denied.")
    
    if userinfo["aud"] != settings.shibboleth_client_id:
        raise HTTPException(status_code=401, detail="Unauthenticated. Access Denied.")
    
    expires = datetime.fromtimestamp(userinfo["exp"])
    
    if expires < datetime.now():
        raise HTTPException(status_code=401, detail="Unauthenticated. Access Denied.")

    return userinfo['email']

async def verify_account(
    user_email = Depends(verify_userinfo),
    postgres: AsyncSession = Depends(dependency=get_postgres_session)
):
    query = select(Account).where(Account.email == user_email)
    result = await postgres.exec(statement=query)
    account = result.one_or_none()
    if account is None:
        raise HTTPException(status_code=401, detail="Unauthenticated. Access Denied.")
    return account