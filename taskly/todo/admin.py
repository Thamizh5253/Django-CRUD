from django.contrib import admin

from .models import Task , Evalution

# Register your models here.

admin.site.register(Task)
admin.site.site_header = 'Taskly Admin'
admin.site.register(Evalution)