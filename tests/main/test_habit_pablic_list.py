from typing import List

import pytest

from main.models import Habit
from main.serializers import HabitSerializer
from tests.factories import HabitFactory


@pytest.mark.django_db
class TestHabitPublicList:
    url: str = '/public_habits/'

    def test_habit_public_list(self, auth_client) -> None:
        habits: List[Habit] = HabitFactory.create_batch(5)

        habit_privat = HabitFactory.create()
        habit_privat.is_public = False
        habit_privat.save(update_fields=["is_public", ])

        expected_response = {
            "count": 5,
            "next": None,
            "previous": None,
            "results": HabitSerializer(habits, many=True).data
        }
        response = auth_client.get(self.url)

        assert response.status_code == 200
        assert response.data == expected_response

    def test_habit_public_list_with_pagination(self, auth_client):
        habits = HabitFactory.create_batch(10)

        habit_privat = HabitFactory.create()
        habit_privat.is_public = False
        habit_privat.save(update_fields=["is_public", ])

        expected_response = {
            "count": 10,
            "next": 'http://testserver/public_habits/?limit=5&offset=5',
            "previous": None,
            "results": HabitSerializer(habits[:5], many=True).data
        }
        response = auth_client.get(self.url)

        assert response.status_code == 200
        assert response.data == expected_response
