from collections import OrderedDict
from hashlib import sha1
from urllib.parse import urlencode

from django.http import HttpRequest

from .http_response_builder import build_http_response
from ..server_context import ServerContext

def ok(request: HttpRequest, server_context: ServerContext):
    '''Indicates that Vanilla
    should log in the user,
    or create an account for them
    with the given username and email.
    '''
    content = _make_response_content(server_context)

    return build_http_response(content, request)

def _make_response_content(server_context: ServerContext) -> OrderedDict:
    result = _content_from_user_data(server_context.user_data)
    _add_fields_to_content(result, server_context.client_id, server_context.secret)

    return result

def _add_fields_to_content(content, client_id, secret):
    content['client_id'] = client_id
    _add_signature_to_content(content, secret)

def _add_signature_to_content(content, secret):
    signature = _make_response_signature(content, secret)

    content['signature'] = signature

def _content_from_user_data(user_data) -> OrderedDict:
    _remove_null_values(user_data)

    return OrderedDict(sorted(user_data.items()))

def _remove_null_values(user_data: dict):
    for key, value in user_data.items():
        if value is None:
            # Vanilla doesn't like null values
            # in its JSON, apparently
            user_data[key] = ""

def _make_response_signature(content, secret):
    query_str = urlencode(content)
    result = sha1(f"{query_str}{secret}").hexdigest()

    return result