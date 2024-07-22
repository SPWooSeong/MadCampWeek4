from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("current-room/", views.current_room, name="current_room"),
    path("make-room/", views.make_room, name="make_room"),
]