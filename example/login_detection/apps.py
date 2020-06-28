from django.apps import AppConfig


class LoginDetectionConfig(AppConfig):
    name = "example.login_detection"

    def ready(self):
        import example.login_detection.signals  # noqa
