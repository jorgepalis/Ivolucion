from django.db import models
from users.models import User

# Create your models here.

class Status(models.Model):
    """Modelo para representar el estado de una tarea"""
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    
class Category(models.Model):
    """Modelo para representar la categoría de una tarea"""
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    
class Task(models.Model):
    """Modelo para representar una tarea"""
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class logTask(models.Model):
    """Modelo para representar el log de una tarea"""
    ACTION_CHOICES = [
        ('CREATED', 'Created'),
        ('UPDATED', 'Updated'),
        ('DELETED', 'Deleted'),
    ]

    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    action = models.CharField(max_length=255, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.timestamp} - {self.action} - {self.task.title}"
