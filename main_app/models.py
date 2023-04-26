from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone


class Job(models.Model):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    requirements = models.CharField(max_length=255)
    salary = models.CharField(max_length=255)
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

class Token(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=40, unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.key