from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'priority', 'is_completed', 'created_at']
        read_only_fields = ['id',]

class MarkCompletedTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'priority', 'is_completed', 'created_at']
        read_only_fields = ['id', 'name', 'description', 'priority', 'created_at']
