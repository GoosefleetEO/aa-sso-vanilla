from django.apps import AppConfig

from .constants import Constants

class ExampleConfig(AppConfig):
    name = Constants.app_name_raw
    label = Constants.app_url
    verbose_name = Constants.readable_name_raw
