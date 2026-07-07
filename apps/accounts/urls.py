from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("activate-account/", views.activate_account, name="activate_account"),
]