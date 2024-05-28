from django.apps import AppConfig


class AuthMmhConfig(AppConfig):
    name = 'auth_mmh_v2'

    def ready(self):
        import auth_mmh_v2.signals
