from django.contrib.auth.decorators import login_required, permission_required

from .responder import Responder

@login_required
@permission_required("example.basic_access")
def sso(request):
    return Responder.handle(request)