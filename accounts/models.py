from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    age = models.IntegerField(null=True, blank=True)
    country = models.CharField(max_length=100, blank=True)


    def __str__(self):
        return f"Name: {self.username} Age: {self.age}"
    
