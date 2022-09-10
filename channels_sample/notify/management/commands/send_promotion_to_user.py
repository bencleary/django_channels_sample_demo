import channels.layers
from asgiref.sync import async_to_sync
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('user_id', nargs="+", type=int)

    def handle(self, *args, **options):
        if options["user_id"]:
            channel_layer = channels.layers.get_channel_layer()
            try:
                user = User.objects.get(id=options["user_id"][0])
                print(user)
                print(2)
                async_to_sync(channel_layer.group_send)(
                        f"user.{user.id}", {"type": "action", "key": "offer", "promotion": f"Here are some crazy deals for you {user.id}"}
                    )
                print(f"Sent offer to {user.id}")
            except Exception as e:
                print(e)
