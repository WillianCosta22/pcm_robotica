from django.apps import AppConfig

class RobotsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'robots'


class RobotSapConfig(AppConfig):
    name = 'robot_sap'

    def ready(self):
        from .init_superuser import create_superuser
        create_superuser()

