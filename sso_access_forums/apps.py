from django.apps import AppConfig

from .constants import Constants, Names

class ExampleConfig(AppConfig):
    name = Names.app_name_raw
    label = Names.app_url
    verbose_name = Constants.readable_name_raw
