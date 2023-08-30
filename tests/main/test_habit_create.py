from typing import Dict, Any
import pytest
from rest_framework.fields import TimeField

from main.models import Habit


@pytest.mark.django_db
class TestHabitCreate:
    url = '/habits/'

    def test_habit_create_without_authorization(self, client) -> None:
        response = client.post(self.url)

        assert response.status_code == 401
        assert response.json() == {'detail': 'Authentication credentials were not provided.'}

    def test_habit_create(self, auth_client) -> None:
        data = {"title": "test10",
                "place": "test_place",
                "time": "23:47",
                "action": "test_action",
                "execution_time": "0:2"}

        response = auth_client.post(self.url, data=data)
        new_habit: Habit = Habit.objects.get()

        assert response.status_code == 201
        assert response.json() == _serializer_response(new_habit)

    def test_habit_create_with_related_habits_and_reward(self, auth_client, habit: Habit) -> None:
        data = {"title": "test10",
                "place": "test_place",
                "time": "23:47",
                "action": "test_action",
                "execution_time": "0:2",
                "related_habit": habit.id,
                "reward": "test"}

        response = auth_client.post(self.url, data=data)

        assert response.status_code == 400
        assert response.json() == {
            'non_field_errors': ['Исключён одновременный выбор связанной привычки и указания вознаграждения.']
        }

    def test_habit_create_with_long_time(self, auth_client) -> None:
        data = {"title": "test10",
                "place": "test_place",
                "time": "23:47",
                "action": "test_action",
                "execution_time": "0:5"}

        response = auth_client.post(self.url, data=data)

        assert response.status_code == 400
        assert response.json() == {'non_field_errors': ['Время выполнения должно быть не больше 120 секунд.']}

    def test_habit_create_with_releted_habit_not_pliasant(self, auth_client, habit) -> None:
        habit.is_pleasant = False
        habit.save(update_fields=['is_pleasant', ])

        data = {"title": "test10",
                "place": "test_place",
                "time": "23:47",
                "action": "test_action",
                "execution_time": "0:2",
                "related_habit": habit.id}

        response = auth_client.post(self.url, data=data)

        assert response.status_code == 400
        assert response.json() == {
            'non_field_errors': ['В связанные привычки могут попадать только привычки с признаком приятной привычки.']
        }

    def test_habit_create_is_pleasant_with_related_habit(self, auth_client, habit) -> None:
        habit.is_pleasant = True
        habit.save(update_fields=['is_pleasant', ])

        data = {"title": "test10",
                "place": "test_place",
                "time": "23:47",
                "action": "test_action",
                "execution_time": "0:2",
                "related_habit": habit.id,
                "is_pleasant": True}

        response = auth_client.post(self.url, data=data)

        assert response.status_code == 400
        assert response.json() == {
            'non_field_errors': ['У приятной привычки не может быть вознаграждения или связанной привычки.']
        }

    def test_habit_create_is_pleasant_with_reward(self, auth_client) -> None:
        data = {"title": "test10",
                "place": "test_place",
                "time": "23:47",
                "action": "test_action",
                "execution_time": "0:2",
                "reward": "test",
                "is_pleasant": True}

        response = auth_client.post(self.url, data=data)

        assert response.status_code == 400
        assert response.json() == {
            'non_field_errors': ['У приятной привычки не может быть вознаграждения или связанной привычки.']
        }

    def test_habit_create_with_low_periodicity(self, auth_client) -> None:
        data = {"title": "test10",
                "place": "test_place",
                "time": "23:47",
                "action": "test_action",
                "execution_time": "0:2",
                "periodicity": 10}

        response = auth_client.post(self.url, data=data)

        assert response.status_code == 400
        assert response.json() == {'non_field_errors': ['Нельзя выполнять привычку реже, чем 1 раз в 7 дней.']}


def _serializer_response(habit: Habit, **kwargs) -> Dict[str, Any]:
    data: Dict[str, Any] = {'id': habit.id,
                            "title": habit.title,
                            "place": habit.place,
                            "time": TimeField().to_representation(habit.time),
                            "action": habit.action,
                            "is_pleasant": habit.is_pleasant,
                            "periodicity": habit.periodicity,
                            "reward": habit.reward,
                            "execution_time": TimeField().to_representation(habit.execution_time),
                            "is_public": habit.is_public,
                            "creator": habit.creator.id,
                            "related_habit": habit.related_habit}

    return data | kwargs
