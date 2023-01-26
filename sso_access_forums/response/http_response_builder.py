import json

from django.http import HttpRequest, HttpResponse

def build_http_response(raw_response: dict, request: HttpRequest) -> HttpResponse:
    response = json.dumps(raw_response)
    content_type = 'application/json'

    if 'callback' in request:
        response = f"{request['callback']}({response})"
        content_type = 'application/javascript'

    return HttpResponse(response, content_type=content_type)