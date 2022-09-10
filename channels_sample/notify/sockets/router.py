from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"^ws/user/(?P<id>\w+)/notifications/$", consumers.UserNotificationsConsumer.as_asgi()),
]
