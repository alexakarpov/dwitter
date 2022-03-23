# dwitter/urls.py

from django.urls import path
from .views import dashboard, profiles, profile

app_name = "dwitter"

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("profiles/", profiles, name="profiles"),
    path("profile/<int:pk>", profile, name="profile"),
]
