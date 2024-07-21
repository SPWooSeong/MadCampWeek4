from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("current_room/", views.current_room, name="current_room"),
]