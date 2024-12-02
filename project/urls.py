# urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, TaskViewSet, add_project_view, edit_project_view, delete_project_view, project_tasks_view, add_task_view, edit_task_view, delete_task_view

router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('rest/', include(router.urls)),
    path('add/', add_project_view, name='add_project'),
    path('edit/<uuid:pk>/', edit_project_view, name='edit_project'),
    path('delete/<uuid:pk>/', delete_project_view, name='delete_project'),
    path('<uuid:project_id>/tasks/', project_tasks_view, name='project_tasks'),
    path('<uuid:project_id>/tasks/new/', add_task_view, name='create_task'),
    path('tasks/<uuid:task_id>/edit/', edit_task_view, name='edit_task'),
    path('tasks/<uuid:task_id>/delete/', delete_task_view, name='delete_task'),
]
