from django.urls import path
from . import views

urlpatterns = [
    path("", lambda r: redirect("/hello/", permanent=False)),
    path("hello/", views.hello_world),
]