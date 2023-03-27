from django.urls import path
from tareas.api.views import (
    UserCreateAPIView, UserReadAPIView, UserUpdateAPIView, UserDestroyAPIView,
    HomeworkCreateAPIView, HomeworkReadAPIView, HomeworkUpdateAPIView, HomeworkDestroyAPIView
)

urlpatterns = [
    path('create-user/', UserCreateAPIView.as_view(), name='create-user'),
    path('read-user/', UserReadAPIView.as_view(), name='read-user'),
    path('update-user/<int:pk>/', UserUpdateAPIView.as_view(), name='update-user'),
    path('delete-user/<int:pk>/', UserDestroyAPIView.as_view(), name='delete-user'),

    path('create-tarea/', HomeworkCreateAPIView.as_view(), name='create-tarea'),
    path('read-tarea/', HomeworkReadAPIView.as_view(), name='read-tarea'),
    path('update-tarea/<int:pk>/', HomeworkUpdateAPIView.as_view(), name='update-tarea'),
    path('delete-tarea/<int:pk>/', HomeworkDestroyAPIView.as_view(), name='delete-tarea'),
]