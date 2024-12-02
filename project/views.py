# views.py
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters as rest_framework_filters
from django_filters import rest_framework as filters

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Project, Task
from .forms import ProjectForm, TaskForm
from django.core.paginator import Paginator
from datetime import date

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    authentication_classes = [TokenAuthentication,]
    ordering = ["updated_at"]
    filter_backends = [
        filters.DjangoFilterBackend,
        rest_framework_filters.OrderingFilter,
        rest_framework_filters.SearchFilter,
    ]
    search_fields = ["id", "name"]


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = [TokenAuthentication,]
    ordering = ["updated_at"]
    filter_backends = [
        filters.DjangoFilterBackend,
        rest_framework_filters.OrderingFilter,
        rest_framework_filters.SearchFilter,
    ]
    search_fields = ["id", "name"]


# Home view: List all projects
@login_required
def home_view(request):
    # Filter projects that have not ended yet and are specific to the logged in user/client
    client = Client.objects.get(user=request.user)
    projects = Project.objects.filter(client=client, end_date__gte=date.today()).order_by('start_date')
    
    # Add pagination
    paginator = Paginator(projects, 6)  # Display 6 projects per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'pages/home.html', {'page_obj': page_obj})

# Add project view
@login_required
def add_project_view(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)  # Don't save to the database yet
            # Get the client associated with the logged-in user first
            try:
                client = Client.objects.get(user=request.user)
                project.client = client  # Associate client with the project
                project.save()  # Save the project instance to the database
                return redirect('home')
            except Client.DoesNotExist:
                form.add_error(None, "Client associated with the user does not exist.")
    else:
        form = ProjectForm()

    return render(request, 'forms/project_form.html', {'form': form, 'action': 'Add'})

# Edit project view
@login_required
def edit_project_view(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'forms/project_form.html', {'form': form, 'action': 'Update'})

# Delete project view
@login_required
def delete_project_view(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project.delete()
    return redirect('home')


# Project view: List all Tasks
def project_tasks_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    tasks = project.tasks.all()
    paginator = Paginator(tasks, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'pages/project_tasks.html', {'project': project, 'page_obj': page_obj})

# Add task view
def add_task_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            return redirect('project_tasks', project_id=project.id)
    else:
        form = TaskForm()
    return render(request, 'forms/task_form.html', {'form': form, 'project': project, 'type': "Add Task"})

# Edit task view
def edit_task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('project_tasks', project_id=task.project.id)
    else:
        form = TaskForm(instance=task)
    return render(request, 'forms/task_form.html', {'form': form, 'task': task, 'type': "Edit Task"})

# Delete task view
def delete_task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    project_id = task.project.id
    task.delete()
    return redirect('project_tasks', project_id=project_id)