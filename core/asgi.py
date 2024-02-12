import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path , re_path
from tic_tac_toe.consumers import *
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = get_asgi_application()


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter([
        path("ws/tic_tac_toe/game/<int:id>", GameConsumer.as_asgi())
        # path("ws/user/tic_tac_toe/game/<int:id>/", GameConsumer.as_asgi())
        # path("ws/game/<int:id>", GameConsumer.as_asgi())
        # re_path(r"^ws/game/(?P<id>[^/]+)/$", GameConsumer.as_asgi()),
    ])
})
