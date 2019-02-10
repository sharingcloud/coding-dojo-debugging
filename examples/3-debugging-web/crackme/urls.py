from django.urls import re_path
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
    re_path(r"^login$", views.login, name="login"),
    re_path(r"^logout$", views.logout, name="logout"),
    re_path(r"^challenge$", views.challenge, name="challenge"),
    re_path(r"^secure$", views.secure, name="secure"),
    re_path(r"^bonus$", views.bonus, name="bonus"),
    re_path(r"^check_code$", views.check_code, name="check_code"),
    re_path(r"", RedirectView.as_view(url='challenge'), name="home"),
]
