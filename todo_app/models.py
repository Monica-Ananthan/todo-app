from django.db import models
import random

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=20, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.color:
            colors = [
                "bg-red-500",
                "bg-yellow-500",
                "bg-green-500",
                "bg-blue-500",
                "bg-purple-500",
                "bg-pink-500"
            ]
            self.color = random.choice(colors)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Task(models.Model):
    title = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    category = models.ForeignKey("Category", on_delete=models.CASCADE, null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
