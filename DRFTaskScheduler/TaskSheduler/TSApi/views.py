from __future__ import annotations
from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.views import APIView
from tutorial.quickstart.serializers import UserSerializer, GroupSerializer
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import pagination
from rest_framework import filters

from django_filters.rest_framework import DjangoFilterBackend as DFB

from .serializers import *
from .models import TaskElectricalModel



class Paginator(pagination.PageNumberPagination):
    page_size = 20
    page_query_param = "page_size"
    max_page_size = 1000


class TaskListView(generics.ListAPIView):
    queryset = TaskElectricalModel.objects.all()
    serializer_class = TasksSerializer
    pagination_class = Paginator
    filter_backends = [DFB, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['street', 'house']
    filterset_fields = ['street', 'house', 'date_registration', 'date_execution', 'apartment']
    ordering_filter = ['street', "house"]


class TaskCreateView(generics.CreateAPIView):
    queryset = TaskElectricalModel.objects.all()
    serializer_class = TasksSerializer


class TaskUpdateView(generics.UpdateAPIView):
    queryset = TaskElectricalModel.objects.all()
    serializer_class = TasksUpdateSerializer
        

class WorkUpdateView(generics.UpdateAPIView):
    """Изминение одной записи, но изменить можно только поля о выполнении заявки"""
    queryset = TaskElectricalModel.objects.all()
    serializer_class = TasksWorkUpdateSerializer


class TaskDetailView(generics.RetrieveAPIView):
    """Отображение одной заявки"""
    queryset = TaskElectricalModel.objects.all()
    serializer_class = TasksSerializer



class TaskDeleteView(generics.DestroyAPIView):
    queryset = TaskElectricalModel.objects.all()
    serializer_class = TasksSerializer










