# FastAPI Dependencies
from fastapi import Request, HTTPException, Depends

# SQLModel Dependencies
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

# Authlib Dependencies
from authlib.integrations.starlette_client import OAuthError

# Local Dependencies
from src.shared import get_postgres_session
from src.shared.auth.types import UserInfo
from src.shared.auth.models import AccountRead, Account
from src.shared.auth.shibboleth import shibboleth

# https://github.com/SogoKato/oidc-fastapi-authlib/blob/main/backend/main.py

async def get_userinfo(request: Request) -> UserInfo:
    try:
        token = await shibboleth.authorize_access_token(request=request)
        userinfo = token.get('userinfo')
        request.session["id_token"] = token.get("id_token")
        return UserInfo.model_validate(userinfo)
    except OAuthError:
        raise HTTPException(status_code=500, detail="Auth Error")

async def authenticate(
    userinfo: UserInfo = Depends(get_userinfo),
    postgres: AsyncSession = Depends(dependency=get_postgres_session)
) -> Account:
    # This might become its own controller which is a dependency here, or at login
    statement = select(Account).where(Account.email == userinfo.email)
    result = await postgres.exec(statement=statement)
    user = result.one_or_none()
    if user is None:
        created_account = Account(
            given_name=userinfo.given_name,
            family_name=userinfo.family_name,
            email=userinfo.email,
            email_verified=userinfo.email_verified
        )

        postgres.add(instance=created_account)

        await postgres.commit()
        await postgres.refresh(instance=created_account)
        return created_account
    return user