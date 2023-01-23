from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render


@login_required
@permission_required("example.basic_access")
def index(request):
    login_button_content = f"<a href='{sso_provider_url}'><img='{login_button_image_path}' alt='Login to EVE SSO Here'></img></a>"
    context = {"login-panel": f"Login to EVE SSO to access the forums.\n{login_button_content}"}
    return render(request, "example/index.html", context)
