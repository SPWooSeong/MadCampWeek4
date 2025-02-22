from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("subject-ranking/", views.subject_ranking, name="subject_ranking"),
    path("subject-ranking/<int:subject_id>/element-ranking/", views.element_ranking, name="element_ranking"),
    path("subject-list/", views.subject_list, name="subject_list"),
    path("elements/<int:room_id>/", views.elements, name="elements"),
    path('winner/<int:element_id>/', views.increment_element_win, name='increment_element_win'),
    path('num-used/<int:room_id>/', views.increment_subject, name='increment_subject'),
    path('new-subject/', views.new_subject, name='new_subject'),
]
