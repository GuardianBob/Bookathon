from django.apps import AppConfig


class LoginappConfig(AppConfig):
    name = 'loginApp'

    def ready(self):
        import loginApp.signals