from fastapi import Depends, Request, HTTPException
from authlib.oidc.core import UserInfo
from authlib.integrations.starlette_client import OAuthError, StarletteOAuth2App
from src.settings import get_settings, Settings
from src.shared.auth.shibboleth import oauth, shibboleth

# https://github.com/SogoKato/oidc-fastapi-authlib/blob/main/backend/main.py

async def authenticate(request: Request):
    try:
        token = await shibboleth.authorize_access_token(request=request)
    except OAuthError:
        raise HTTPException(status_code=500, detail="Auth Error")
    finally:
        userinfo: UserInfo = await shibboleth.parse_id_token(request=request, token=token)
        # Check Database
        request.session["id_token"] = token.get("id_token")
        return userinfo