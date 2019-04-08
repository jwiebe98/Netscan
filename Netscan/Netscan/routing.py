from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator

#Import Consumers
from home.consumers import HomeConsumer, SettingsConsumer

#Similar to urls.py, this routes urls to consumers.
application = ProtocolTypeRouter({
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                [
                    #path('home/', index.as_view(), name='home'),
                    url(r"^home", HomeConsumer),
                    url(r"^settings", SettingsConsumer)
                ]
            )
        )
    )
})
