from django.apps import AppConfig
from apps.utils.print_colors import _orange


class BaseConfig(AppConfig):
    name = 'apps.app'
    verbose_name = 'Tutorias'

    def ready(self):
        print(_orange('Ready App!'))
        from . import signals