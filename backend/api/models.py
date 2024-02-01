from django.contrib.auth.models import User
from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Step(TimeStampedModel):
    CHOICES = (
        ('G', 'greeting'),
        ('Q', 'question'),
        ('E', 'end'),
    )
    name = models.CharField(max_length=1, choices=CHOICES, default='G')
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Log(TimeStampedModel):
    CHOICES = (
        ('U', 'user'),
        ('C', 'chat'),
    )
    text = models.TextField()
    sender = models.CharField(max_length=1, choices=CHOICES)
    step = models.ForeignKey(Step, on_delete=models.CASCADE)
