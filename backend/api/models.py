from django.contrib.auth.models import User
from django.db import models


class TimeStampedModel(models.Model):
    """
    An abstract base model providing timestamp fields for creation and last update.

    Attributes:
    - created_at (datetime): The timestamp of when the instance was created.
    - updated_at (datetime): The timestamp of the last update to the instance.

    Meta:
    - abstract (bool): Indicates that this model is abstract and won't create a database table.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Step(TimeStampedModel):
    """
    Model representing a step in a chat conversation.

    Attributes:
    - name (str): The name of the step, chosen from predefined choices ('G' for greeting, 'Q' for question, 'E' for end).
    - user (ForeignKey to User): The user associated with this step.
    """

    CHOICES = (
        ('G', _('Greeting')),
        ('Q', _('Question')),
        ('E', _('End')),
    )
    name = models.CharField(max_length=1, choices=CHOICES, default='G')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Step {self.get_name_display()} for User {self.user.username} (created at {self.created_at})"

    def __repr__(self):
        return f"<Step: {self.get_name_display()} - User: {self.user.username} - Created at: {self.created_at}>"

    class Meta:
        ordering = ("-created_at",)


class Log(TimeStampedModel):
    """
    Model representing a log entry in a chat conversation.

    Attributes:
    - text (str): The text content of the log entry.
    - sender (str): The sender type ('U' for user, 'C' for chat).
    - step (ForeignKey to Step): The step associated with this log entry.
    """
    CHOICES = (
        ('U', 'user'),
        ('C', 'chat'),
    )
    text = models.TextField()
    sender = models.CharField(max_length=1, choices=CHOICES)
    step = models.ForeignKey(Step, on_delete=models.CASCADE)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f'Log, {self.text}'

    def __repr__(self):
        return f"<Log: {self.text} {self.created_at}>"
