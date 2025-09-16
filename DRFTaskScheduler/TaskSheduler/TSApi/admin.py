from django.contrib import admin
from .models import TaskElectricalModel

class TaskElectricalAdmin(admin.ModelAdmin):
    exclude = ["date_creation"]
    list_display = ("pk", "date_creation", "date_registration", "street", "house", "apartment", "is_complited")
    ordering = ["-date_registration", "street", "house"]
    list_display_links = ["pk", "street", "house"]
    list_per_page = 10
    search_fields = ["street", "house", "apartment"]
    list_filter = ["street", "house", "apartment"]

    def is_complited(self, task: TaskElectricalModel):
        return f"{task.date_execution}" if task.complited_work and task.date_execution else "Не выполнена"


admin.site.register(TaskElectricalModel, TaskElectricalAdmin)
