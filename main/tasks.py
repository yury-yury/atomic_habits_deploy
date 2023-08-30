from django.conf import settings
from telebot import TeleBot

from atomic_habits.celery import app
from main.models import Habit


@app.task
def send_telegram_message(habit_id: int) -> None:
    """
    The send_telegram_message function takes the habit id from the database as an integer parameter.
    When called, it sends a reminder about completing the habit to the Telegram account
    of the user who created the habit.
    """
    habit = Habit.objects.get(id=habit_id)
    bot = TeleBot(settings.TG_TOKEN)
    message: str = f"Напоминание о выполнении привычки {habit.action} в {habit.time} в {habit.place}"
    bot.send_message(habit.creator.chat_id, message)
