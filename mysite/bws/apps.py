from django.apps import AppConfig


class BwsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bws'

    def ready(self):
        from .signals import create_profile, save_profile




