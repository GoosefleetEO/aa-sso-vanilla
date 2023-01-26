from typing import Dict

from django.contrib.auth.decorators import login_required, permission_required

from .response import ok, failed
from .server_context import ServerContext
from .validate_request import validate_request

@login_required
@permission_required("example.basic_access")
def sso(request):
    try:
        server_context = ServerContext.get_server_context()
        validate_request(request, server_context)

        return ok(request, server_context)
    except Exception as e:
        log_exception(e)
        return failed(request, str(e))

def log_exception(exception):
    pass