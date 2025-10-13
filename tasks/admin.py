from django.contrib import admin
from .models import Task, Status, Category, logTask

# Register your models here.
admin.site.register(Task)
admin.site.register(Status)
admin.site.register(Category)
admin.site.register(logTask)
