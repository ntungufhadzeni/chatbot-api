from django.contrib.auth.models import User
from django.db import models


class Step(models.Model):
    CHOICES = (
        ('G', 'greeting'),
        ('Q', 'question'),
        ('E', 'end'),
    )
    name = models.CharField(max_length=1, choices=CHOICES, default='G')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def next_step(self):
        if self.name == 'G':
            return 'Q'
        elif self.name == 'Q':
            return 'E'
        elif self.name == 'E':
            return 'G'


class ChatLog(models.Model):
    CHOICES = (
        ('U', 'user'),
        ('C', 'chat'),
    )
    text = models.TextField()
    sender = models.CharField(max_length=1, choices=CHOICES)
    step = models.ForeignKey(Step, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
