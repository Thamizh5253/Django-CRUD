from django.db import models


# Task Model (Connected to User)
class Task(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed')
    ]
    title = models.CharField(max_length=100)
    status = models.CharField(max_length=14, choices=STATUS_CHOICES, default='Pending')
    date = models.DateField(auto_now_add=True)

    # ForeignKey to link Task to a User

    def __str__(self):
        return self.title  # Display task title in admin panel

class Evalution(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    marks = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="evalutions")

    def __str__(self):
        return self.name