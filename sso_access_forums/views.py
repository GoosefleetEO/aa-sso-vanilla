from typing import Dict

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render

from .constants import Paths


@login_required
@permission_required("example.basic_access")
def index(request):
    login_button_content = f"<a href='{Paths.sso_provider}'><img='{Paths.login_button_image}' alt='Login to EVE SSO Here'></img></a>"
    context = {"login-panel": f"Login to EVE SSO to access the forums.\n{login_button_content}"}
    return render(request, "example/index.html", context)

class _Keys:
    callback_url = "redirect"
    client_id = "client_id"
    scope = "scope"
    state = "state"

@login_required
@permission_required("example.basic_access")
def _build_sso_url(request) -> str:
    # Redirect your user to https://login.eveonline.com/v2/oauth/authorize/ with the following parameters in the query string.
    params = _makeParameterDict(request)
    return f"https://login.eveonline.com/v2/oauth/authorize/?response_type=code&redirect_uri={params[_Keys.callback_url]}&client_id={params[_Keys.client_id]}&scope={params[_Keys.scope]}&state={params[_Keys.state]}"

def _makeParameterDict(request) -> Dict[str, str]:
    result = _retrieveFieldsForRequest(request)
    
    for (key, value) in result:
        result[key] = _urlEncode(value)

    return result

def _retrieveFieldsForRequest(request) -> Dict[str, str]:
    result = _dictForFieldsInClass(_Keys)
    
    raise NotImplementedError()

    return result

def _urlEncode(input_text) -> str:
    raise NotImplementedError()

def _dictForFieldsInClass(target_class) -> Dict[str, str]:
    fields = [f for f in vars(target_class) if not f.startswith('__')]
    
    return {f: "" for f in fields}