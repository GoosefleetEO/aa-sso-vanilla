import logging

from .response import ok, failed
from .server_context import ServerContext
from .validate_request import validate_request

_logger = logging.getLogger(__name__)

class Responder():
    '''
    '''

    @classmethod
    def handle(cls, request):
        try:
            return cls._send_ok(request)
        except Exception as e:
            return cls._send_failed(request, e)

    @classmethod
    def _send_ok(cls, request):
        server_context = ServerContext.get_server_context()
        validate_request(request, server_context)

        return ok(request, server_context)

    @classmethod
    def _send_failed(cls, request, exception: Exception):
        cls._log_exception(exception)
        return failed(request, str(exception))

    @classmethod
    def _log_exception(cls, exception: Exception):
        _logger.error("SSO validation failed! Exception info in following message:")
        _logger.exception(exception)