from django.urls import path
from .views import google_login_callback
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('google/login/callback/', google_login_callback, name='google_login_callback'),

]