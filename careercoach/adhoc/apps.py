from django.apps import AppConfig


class AdhocConfig(AppConfig):
    name = 'adhoc'

    def ready(self):
        import adhoc.signals

