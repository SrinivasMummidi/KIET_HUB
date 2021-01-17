from django.contrib import admin
from .models import Task, TaskResponse

# Register your models here.
admin.site.register(Task)
admin.site.register(TaskResponse)