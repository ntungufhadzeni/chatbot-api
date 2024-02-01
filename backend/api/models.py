from django.contrib.auth.models import User
from django.db import models


class Step(models.Model):
    CHOICES = (
        ('G', 'greeting'),
        ('Q', 'question'),
        ('E', 'end'),
    )
    name = models.CharField(max_length=1, choices=CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Log(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    step = models.ForeignKey(Step, on_delete=models.CASCADE)
