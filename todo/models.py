from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Task(models.Model):
    class Priority(models.IntegerChoices):
        PRIORITY_1 = 1, _('Priority 1')
        PRIORITY_2 = 2, _('Priority 2')
        PRIORITY_3 = 3, _('Priority 3')
        PRIORITY_4 = 4, _('Priority 4')

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    priority = models.IntegerField(choices=Priority.choices, default=Priority.PRIORITY_4)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Tasks are ordered by priority and date created
        ordering = ['priority', '-created_at']

    def __str__(self):
        return f"{self.name} ({self.get_priority_display()})"
