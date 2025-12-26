from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'core'



    def ready(self):
        from .signals import assign_pro_plan
