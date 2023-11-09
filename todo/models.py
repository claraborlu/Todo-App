from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Task(models.Model):
    PRIORITY_CHOICES = (
    ('P1', 'Priority 1'),
    ('P2', 'Priority 2'),
    ('P3', 'Priority 3'),
    ('P4', 'Priority 4'),
)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=2, choices=PRIORITY_CHOICES, default='P4')
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Tasks are ordered by priority and date created
        ordering = ['priority', '-created_at']

    def __str__(self):
        return f"{self.name} ({self.get_priority_display()})"
