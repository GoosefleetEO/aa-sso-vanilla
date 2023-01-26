from django.urls import path

from . import views
from .constants import Names

app_name = Names.app_url

urlpatterns = [
    path(f'/{app_name}', views.sso, name=app_name),
]