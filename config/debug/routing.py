from channels.auth import AuthMiddlewareStack
from channels.routing import (
    ProtocolTypeRouter,
    URLRouter,
)
from channels.security.websocket import OriginValidator
from django.conf import settings

from ses.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    # No acepta conexiones distintas a las del websocket
    'websocket': OriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                websocket_urlpatterns,
            ),
        ),
        settings.WS_ALLOWED_HOSTS,
    ),
})
