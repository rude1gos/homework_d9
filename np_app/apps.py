from django.apps import AppConfig


class NpAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'np_app'

    def ready(self):
        import np_app.signals