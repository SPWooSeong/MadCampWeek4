from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("current-room/", views.current_room, name="current_room"),
    path("make-room/", views.make_room, name="make_room"),
    path("exit-room/", views.exit_room, name="exit_room"),
    path('enter-room/', views.enter_room, name='enter_room'),
]