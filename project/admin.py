from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'client', 'start_date', 'end_date', 'created_at', 'updated_at', 'created_by', 'updated_by')
    search_fields = ('name', )

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'project', 'status', 'created_at', 'updated_at', 'created_by', 'updated_by')
    search_fields = ('name', 'project__name')