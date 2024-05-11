from fastapi import Depends, Request, HTTPException
from starlette.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuthError, StarletteOAuth2App
from src.shared.auth.shibboleth import oauth, shibboleth

# GET: http://localhost:8000/accounts/login
# https://dbrucknr.ngrok.io/accounts/login
async def login(request: Request) -> RedirectResponse:
    redirect_uri = request.url_for('authenticate')
    https_redirect_uri = redirect_uri.replace(scheme="https")
    return await shibboleth.authorize_redirect(
        request=request, 
        redirect_uri=https_redirect_uri
    )

