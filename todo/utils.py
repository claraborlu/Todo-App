from datetime import datetime, timedelta
from django.db.models import Q
from django.utils import timezone

def calculate_weekly_report(user):
    # Find the most recent Monday
    today = timezone.localdate()
    start_of_week = today - timedelta(days=today.weekday())

    # Initialize the report data structure
    report_data = {
        'days': {},
        'total_task_completed': 0,
        'total_task_uncompleted': 0,
        'Weekly_completion_rate': 0
    }

    # Annotate tasks based on completion status for each day of the week
    for i in range(7):
        day = start_of_week + timedelta(days=i)
        day_name = day.strftime('%A')
        tasks_for_day = user.tasks.filter(created_at__date=day)
        total_tasks = tasks_for_day.count()
        completed_count = tasks_for_day.filter(is_completed=True).count()
        uncompleted_count = tasks_for_day.filter(is_completed=False).count()

        # Calculate percentages and round to the nearest whole number
        completed_task_percentage = round((completed_count / total_tasks * 100)) if total_tasks else 0
        uncompleted_task_percentage = round((uncompleted_count / total_tasks * 100)) if total_tasks else 0

        # Update the report data
        report_data['days'][day_name] = {
            'completed_task_percentage': completed_task_percentage,
            'uncompleted_task_percentage': uncompleted_task_percentage
        }
        report_data['total_task_completed'] += completed_count
        report_data['total_task_uncompleted'] += uncompleted_count

    # Calculate the overall completion rate for the week and round to the nearest whole number
    total_tasks_week = report_data['total_task_completed'] + report_data['total_task_uncompleted']
    if total_tasks_week > 0:
        report_data['weekly_completion_rate'] = round((report_data['total_task_completed'] / total_tasks_week) * 100)

    return report_data
