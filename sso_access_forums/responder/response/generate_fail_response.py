from django.http import HttpRequest, HttpResponse

from .http_response_builder import build_http_response

def failed(request: HttpRequest, reason: str) -> HttpResponse:
    '''Indicates that Vanilla
    should reject the user.
    '''
    content = {
        'error': 'invalid_request',
        'message': reason
    }

    return build_http_response(content, request)
