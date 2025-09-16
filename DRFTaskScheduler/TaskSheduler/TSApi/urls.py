from django.contrib import admin
from django.urls import path, include


from . views import *

urlpatterns = [
    path("drf-auth/", include("rest_framework.urls")),
    path("tasks/", TaskListView.as_view()), # список заявок
    path("new/", TaskCreateView.as_view()), # создание новой заявки
    path("updtask/<int:pk>/", TaskUpdateView.as_view()), # обновить поля самой заявки
    path("updwork/<int:pk>/", WorkUpdateView.as_view()), # обновить поля выполненных работ
    path("task/<int:pk>/", TaskDetailView.as_view()), # одна заявка
    path("delete/<int:pk>/", TaskDeleteView.as_view()), # удаление одной заявки
]