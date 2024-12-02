import uuid
from django.db import models
from taskmanagement.base import BaseModel
from user.models import Client

# Create your models here.

class Project(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


class Task(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')

    STATUS_CHOICES = [
        ('TODO', 'To Do'),
        ('WIP', 'Work In Progess'),
        ('ONHOLD', 'On Hold'),
        ('DONE', 'Done'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='TODO')

    def __str__(self):
        return self.name