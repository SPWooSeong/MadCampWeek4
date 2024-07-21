from django.urls import path
from .views import google_login_callback
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('google/login/callback/', google_login_callback, name='google_login_callback'),
    path('mypage/', views.get_user_profile, name='mypage'),
    path('update/', views.update_nickname, name='update'),
]