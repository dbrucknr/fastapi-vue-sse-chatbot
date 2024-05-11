from src.settings import get_settings
from authlib.integrations.starlette_client import OAuth, StarletteOAuth2App

oauth = OAuth()

oauth.register(
    name='umich',
    client_id=get_settings().shibboleth_client_id,
    client_secret=get_settings().shibboleth_client_secret,
    server_metadata_url='https://shibboleth.umich.edu/.well-known/openid-configuration',
    client_kwargs = {
        'scope': 'openid info profile email address phone edumember'
    },
    token_endpoint_auth_method='client_secret_post'
)

shibboleth: StarletteOAuth2App = oauth.create_client('umich')