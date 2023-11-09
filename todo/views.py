from datetime import date, timedelta
from django.utils import timezone
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Task
from .serializers import TaskSerializer, MarkCompletedTaskSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView, UpdateAPIView
from .permissions import IsOwnerOrSuperuser
from .utils import calculate_weekly_report


class AddTaskView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            response_data = {
                'message': 'Task created successfully.',
                'task': serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class TaskListView(ListAPIView):
    serializer_class = TaskSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        today = timezone.localdate()
        tasks_today = Task.objects.filter(user=request.user, created_at__date=today, is_completed=False)
        today_serializer = self.get_serializer(tasks_today, many=True)
        response_data = today_serializer.data
        
        # if today.weekday() != 0:
        #     yesterday = today - timedelta(days=1)
        #     uncompleted_tasks_yesterday = Task.objects.filter(
        #         user=request.user, 
        #         created_at__date=yesterday, 
        #         is_completed=False
        #     )
        #     if uncompleted_tasks_yesterday.exists():
        #         yesterday_serializer = self.get_serializer(uncompleted_tasks_yesterday, many=True)
        #         response_data['Yesterday'] = yesterday_serializer.data

        return Response(response_data)

    def get_queryset(self):
        return Task.objects.none()
    

class UpdateDeleteTaskView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrSuperuser]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Task.objects.all()
        return Task.objects.filter(user=user)
    
class MarkTaskCompletedView(UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = MarkCompletedTaskSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrSuperuser]

    def patch(self, request, *args, **kwargs):
        task = self.get_object()
        task.is_completed = not task.is_completed
        task.save()
        return Response(self.get_serializer(task).data, status=status.HTTP_200_OK)
    
class WeeklyReportView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        report = calculate_weekly_report(request.user)
        return Response(report)