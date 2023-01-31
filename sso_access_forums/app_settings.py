import logging

from django.conf import settings
from decouple import config

from .constants import Names

_logger = logging.Logger(__name__)

# put your app settings here

def _get_config_value(key: str, cast: any, default_value=None) -> any:
    try:
        try:
            return _get_django_value(key)
        except:
            _logger.warning(f"Failed to get setting '{key}' from Django, searching .env and environment variables")
            return _get_decouple_value(key, cast)
    except Exception as e:
        if not default_value:
            raise e
        return default_value

def _get_django_value(key: str) -> any:
    return getattr(settings, key)

def _get_decouple_value(key: str, cast: any) -> any:
    return config(key, cast=cast)

JSCONNECT_CLIENT_ID = _get_config_value(Names.Vars.jsconnect_client_id, str)
JSCONNECT_SECRET = _get_config_value(Names.Vars.jsconnect_secret, str)
ENCRYPTION_SECRET = _get_config_value(Names.Vars.encryption_secret, bytes)