from django.apps import AppConfig


class BotsConfig(AppConfig):
    name = 'Bots'

    def ready(self):
        import Bots.signals
