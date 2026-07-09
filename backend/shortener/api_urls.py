from django.urls import path
from . import views

urlpatterns = [
    path("shorten/", views.shorten_url, name="shorten-url"),
    path("pro/shorten/", views.shorten_pro_url, name="shorten-pro-url"),
]