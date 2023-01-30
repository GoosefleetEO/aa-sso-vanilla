import logging

from django.conf import settings
from decouple import config

_logger = logging.Logger(__name__)

# put your app settings here

def _get_config_value(key: str, default_value=None) -> any:
    try:
        try:
            return _get_django_value(key)
        except:
            _logger.warning(f"Failed to get setting '{key}' from Django, searching .env and environment variables")
            return _get_config_value(key)
    except Exception as e:
        if not default_value:
            raise e
        return default_value

def _get_django_value(key: str) -> any:
    return getattr(settings, key)

def _get_config_value(key: str) -> any:
    return config(key)

JSCONNECT_CLIENT_ID = _get_config_value("JSCONNECT_CLIENT_ID")
JSCONNECT_SECRET = _get_config_value("JSCONNECT_SECRET")