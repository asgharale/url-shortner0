from django.urls import path
from . import views

urlpatterns = [
    path("shorten/", views.shorten_url, name="shorten-url"),
    path("pro/shorten/", views.shorten_pro_url, name="shorten-pro-url"),
    path("wheel/redirect/", views.latest_wheel_redirect, name="latest-wheel-redirect"),
    path("<str:short_code>", views.redirect_short_code, name="redirect-short-code"),
]