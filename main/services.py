from django_celery_beat.models import CrontabSchedule, PeriodicTask

from main.models import Habit


def create_habit_schedule(habit: Habit) -> None:
    """
    The create_habit_schedule function takes an instance of the Habit class as a parameter.
    When called, it generates a launch schedule and the task itself for execution according to the schedule.
    """
    crontab_schedule, _ = CrontabSchedule.objects.get_or_create(
            minute=habit.time.minute,
            hour=habit.time.hour,
            day_of_month=f'*/{habit.periodicity}',
            month_of_year='*',
            day_of_week='*',
        )

    PeriodicTask.objects.create(
        crontab=crontab_schedule,
        name=f'Habit Task - {habit.title}',
        task='main.tasks.send_telegram_message',
        args=[habit.id]
    )
