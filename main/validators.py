from typing import Dict, Any

from rest_framework import serializers
from datetime import time


def habit_validators(value: Dict[str, Any]) -> None:
    """
    The habit_validators function is intended for data validation when creating and modifying objects
    of the Habit class. Takes a dictionary with data as a parameter. When called, it validates the data
    and if the conditions are violated, it raises a ValidationError.
    """
    if value.get('related_habit') and value.get('reward'):
        raise serializers.ValidationError('Исключён одновременный выбор связанной привычки и указания вознаграждения.')

    if value.get('execution_time') > time(00, 2):
        raise serializers.ValidationError('Время выполнения должно быть не больше 120 секунд.')

    if 'related_habit' in value.keys() and not value.get('related_habit').is_pleasant:
        raise serializers.ValidationError('В связанные привычки могут попадать только привычки с признаком приятной '
                                          'привычки.')

    if (value.get('is_pleasant') and value.get('related_habit')) or (value.get('is_pleasant') and value.get('reward')):
        raise serializers.ValidationError('У приятной привычки не может быть вознаграждения или связанной привычки.')

    if value.get('periodicity', 1) > 7:
        raise serializers.ValidationError('Нельзя выполнять привычку реже, чем 1 раз в 7 дней.')
