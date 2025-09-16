from django.contrib import admin
from django.urls import path, include
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.conf.urls.static import static


from . views import *

cache_time = 10


urlpatterns = [
    path("login/", LoginUser.as_view(), name="tssite_login"),
    path('logout/', logout_user, name='tssite_logout'),
    path('register/', RegisterUserView.as_view(), name='tssite_register'),

    path("", cache_page(cache_time)(TasksListView.as_view()), name="tasks"),
    path("notcompl/", cache_page(cache_time)(NotCompletedTaskList.as_view()), name="not_completed"),
    path("completed/", cache_page(cache_time)(CompletedTaskList.as_view()), name="completed_work"),

    path("searchcompl/", cache_page(cache_time)(SearchFromCompletedList.as_view()), name="search_completed"),
    path("searchnotcompl/", cache_page(cache_time)(SearchFromNotCompleted.as_view()), name="search_notcompleted"),
    path("search/", cache_page(cache_time)(SearchListView.as_view()), name="search"),

    path("detail/<int:task_id>", DetailTask.as_view(), name="detail_task"),
    path("newtask/", CreateTask.as_view(), name="createtask"),
    path("workupd/<int:task_id>", UpdateWork.as_view(), name="upd_work"),
    path("taskupd/<int:task_id>", UpdateTask.as_view(), name="upd_task"),

    path("delete/<int:task_id>", DeleteTask.as_view(), name="del_task"),
]