from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import redirect
from django.views import View
from django.views.generic import DetailView, ListView, UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.forms import BaseModelForm
from django.contrib.auth import logout
from django.contrib.auth import login
from django.db.models import Q

from copy import deepcopy

from TSApi.models import *
from .forms import *


menu = [
    {"punkt_menu": "Все заявки", "url_name": "tasks", "active": True},
    {"punkt_menu": "Не выполненые", "url_name": "not_completed", "active": True},
    {"punkt_menu": "Выполненые", "url_name": "completed_work", "active": True},
    {"punkt_menu": "Новая заявка", "url_name": "createtask", "active": True},
]

queryset_list = []
        
head_name = 'Заявки на работы по электрике'


class TasksListView(ListView):
    """Список всех заявок"""
    model = TaskElectricalModel
    template_name = "TSSite/tasklist.html"
    context_object_name = "content"
    paginate_by = 20
    m = deepcopy(menu)
    m[0]["active"] = False
    extra_context = {
            "title": "Список всех заявок",
            "head_name": head_name,
            "menu": m,
            "url_search": "search"
        }
    
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['name_page'] = "all_tasks"
        return context


class SearchListView(ListView):
    """Список всех (выполненых и не выполненых) найденых заявок"""
    model = TaskElectricalModel
    template_name = "TSSite/tasklist.html"
    context_object_name = "content"
    paginate_by = 20
    extra_context = {
            "title": "Список всех заявок",
            "head_name": head_name,
            "menu": menu,
            "url_search": "search"
        }

    def get_queryset(self) -> QuerySet[Any]:
        req = self.request.GET.get("q")
        req = req if not req else req.title()
        queryset = TaskElectricalModel.objects.filter(Q(street__contains=req) | Q(house=req) | Q(apartment=req))
        return queryset
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get("q")
        context['h'] = self.request.GET.get("h")
        return context


class CompletedTaskList(ListView):
    """список выполненых заявок"""
    # model = TaskElectricalModel
    template_name = "TSSite/tasklist.html"
    context_object_name = "content"
    paginate_by = 20
    m = deepcopy(menu)
    m[2]['active'] = False
    extra_context = {
            "title": "Выполненные заявки",
            "head_name": head_name,
            "menu": m,
            "url_search": "search_completed"
        }
    
    def get_queryset(self) -> QuerySet[Any]:
        return TaskElectricalModel.objects.filter(date_execution__regex=r"\d\d\.\d\d\.\d\d\d\d")


class SearchFromCompletedList(ListView):
    """список найденых заявок среди выполненных"""
    model = TaskElectricalModel
    template_name = "TSSite/tasklist.html"
    context_object_name = "content"
    extra_context = {
            "title": "Поиск выполненных заявок",
            "head_name": head_name,
            "menu": menu,
            "name_page": "completed",
            "url_search": "search_completed"
        }
    
    def get_queryset(self) -> QuerySet[Any]:
        req = self.request.GET.get("q")
        req = req if not req else req.title()
        q1 = TaskElectricalModel.objects.filter(Q(street__contains=req) | Q(house=req) | Q(apartment=req))
        q2 = q1.filter(date_execution__regex=r"\d\d\.\d\d\.\d\d\d\d")
        return q2

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get("q")
        return context


class NotCompletedTaskList(ListView):
    """список не выполненых заявок"""
    template_name = "TSSite/tasklist.html"
    context_object_name = "content"
    paginate_by = 20
    m = deepcopy(menu)
    m[1]['active'] = False
    extra_context = {
            "title": "Не выполненные заявки",
            "head_name": head_name,
            "menu": m,
            "name_page": "completed",
            "url_search": "search_notcompleted"
        }
    
    def get_queryset(self) -> QuerySet[Any]:
        return TaskElectricalModel.objects.exclude(date_execution__regex=r"\d\d\.\d\d\.\d\d\d\d")


class SearchFromNotCompleted(ListView):
    """список найденых заявок среди не выполненых"""
    model = TaskElectricalModel
    template_name = "TSSite/tasklist.html"
    context_object_name = "content"
    extra_context = {
            "title": "Поиск не выполненных заявок",
            "head_name": head_name,
            "menu": menu,
            "name_page": "completed",
            "url_search": "search_notcompleted"
        }
    
    def get_queryset(self) -> QuerySet[Any]:
        req = self.request.GET.get("q")
        if req: req = req.title()
        q1 = TaskElectricalModel.objects.filter(Q(street__contains=req) | Q(house=req) | Q(apartment=req))
        q2 = q1.exclude(date_execution__regex=r"\d\d\.\d\d\.\d\d\d\d")
        return q2

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        q = self.request.GET.get("q")
        context['q'] = self.request.GET.get("q")
        return context



class CreateTask(CreateView):
    """Создание новой заявки"""
    form_class = TaskForm
    template_name = "TSSite/createtask.html"
    context_object_name = "content"
    # permission_required = "TSSite.add_TaskElectricalModel"
    m = deepcopy(menu)
    m[3]['active'] = False
    extra_context = {
            "title": "Новая аявка",
            "menu": m,
            "head_name": head_name
        }


class UpdateTask(UpdateView):
    model = TaskElectricalModel
    form_class = TaskUpdateForm
    template_name = "TSSite/createtask.html"
    pk_url_kwarg = "task_id"
    context_object_name = "content"
    extra_context = {
            "title": "Редактирование заявки",
            "menu": menu,
            "head_name": head_name
        }


class DetailTask(DetailView):
    """отображение одной заявки"""
    model = TaskElectricalModel
    template_name = "TSSite/detail_task.html"
    pk_url_kwarg = "task_id"
    context_object_name = "content"
    extra_context = {
            "title": "Заявка",
            "menu": menu,
            "head_name": head_name
        }
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        task = kwargs.get("object")
        if task:
            head = f"ул. {task.street}  д. {task.house}"
            if task.apartment:
                head += f"  кв. {task.apartment}"
            context["head_name"] = head_name
            context["task_id"] = task.pk
        return context

class UpdateWork(UpdateView):
    """Добавлени или изминение выполненых работ"""
    form_class = WorkUpdateForm
    model = TaskElectricalModel
    template_name = "TSSite/updateworks.html"
    pk_url_kwarg = "task_id"
    context_object_name = "content"
    extra_context = {
            "title": "Добавление выполненых работ",
            "menu": menu,
            "head_name": head_name
        }
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context
    


class DeleteTask(DeleteView):
    model = TaskElectricalModel
    success_url = reverse_lazy('tasks')
    pk_url_kwarg = "task_id"
    context_object_name = "content"
    template_name = "TSSite/delete.html"
    extra_context = {
            "title": "Удаление",
            "menu": menu,
            "head_name": head_name
        }


class RegisterUserView(CreateView):
    form_class = RegisterUserForm
    template_name = "TSSite/register.html"
    # context_object_name = "form"
    extra_context = {
        "title": "регистрация",
    }
    success_url = reverse_lazy('tssite_login')

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        user = form.save()
        login(self.request, user)
        return redirect('tasks')


class LoginUser(LoginView):
    ...
    form_class = LoginUserForm
    template_name = "TSSite/login.html"

    extra_context = {
        "title": "авторизация",
        "head_name": head_name
    }

    def get_success_url(self) -> str:
        return reverse_lazy('tasks')



def logout_user(request):
    logout(request)
    return redirect('tssite_login')








