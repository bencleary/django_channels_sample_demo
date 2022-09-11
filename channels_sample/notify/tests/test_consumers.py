from django.urls import reverse_lazy

import pytest
from channels.testing import WebsocketCommunicator
from notify.sockets import consumers, router
from django.contrib.auth.models import User
from channels.routing import URLRouter
from django.core.management import call_command
from asgiref.sync import sync_to_async

pytestmark = pytest.mark.django_db


@pytest.fixture()
def user():
    return User.objects.create(
        username="test_user_1",
        first_name="test",
        last_name="user",
        email="test_user_1@somedomain.com",
    )


@pytest.fixture(autouse=True)
def use_dummy_cache_backend(settings):
    settings.CHANNEL_LAYERS = {
        "default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}
    }


@pytest.mark.asyncio
async def test_notifications_consumer_connects(user):
    communicator = WebsocketCommunicator(
        URLRouter(router.websocket_urlpatterns), f"/ws/user/{user.id}/notifications/"
    )
    connected, _ = await communicator.connect()
    assert connected
    await communicator.disconnect()


@pytest.mark.asyncio
async def test_can_send_offer(user):
    communicator = WebsocketCommunicator(
        URLRouter(router.websocket_urlpatterns), f"/ws/user/{user.id}/notifications/"
    )
    connected, _ = await communicator.connect()
    assert connected
    promotion = "some crazy offer!"
    await communicator.send_to(
        text_data='{"type": "action", "key": "offer", "promotion": "some crazy offer!"}'
    )
    response = await communicator.receive_from()
    assert response == promotion
    await communicator.disconnect()

