from django.apps import AppConfig


class AuthSysConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auth_sys'

    def ready(self):
        import auth_sys.signals
