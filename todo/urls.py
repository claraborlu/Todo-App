from django.urls import path
from .views import (AddTaskView, TaskListView, 
                    UpdateDeleteTaskView, MarkTaskCompletedView,
                    WeeklyReportView,)

urlpatterns = [
    path('', TaskListView.as_view(), name='list_tasks'),
    path('add-task/', AddTaskView.as_view(), name='add_task'),
    path('task/<int:pk>/', UpdateDeleteTaskView.as_view(), name='update-delete-task'),
    path('task/<int:pk>/completed/', MarkTaskCompletedView.as_view(), name='mark-task-completed'),
    path('weekly-report/', WeeklyReportView.as_view(), name='weekly-report'),
]
