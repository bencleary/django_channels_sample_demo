from django.views.generic import TemplateView


class NotificationView(TemplateView):
    template_name = "notify/client.html"
