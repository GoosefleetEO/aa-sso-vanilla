from django.urls import path

from . import views
from .constants import Constants

app_name = Constants.app_url

urlpatterns = [
    path("", views.index, name="index"),
]
