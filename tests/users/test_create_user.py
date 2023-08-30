from typing import Dict, Any
import pytest

from users.models import User


@pytest.mark.django_db
class TestUserCreate:
    url: str = '/user/signup'

    def test_user_create(self, client) -> None:
        data = {"username": "test_username",
                "password": "test_password",
                "password_repeat": "test_password"}
        response = client.post(self.url, data=data)

        new_user = User.objects.get()

        assert response.status_code == 201
        assert response.json() == _serializer_response(new_user)

    def test_user_create_without_username(self, client) -> None:
        data = {"password": "test_password",
                "password_repeat": "test_password"}
        response = client.post(self.url, data=data)

        assert response.status_code == 400
        assert response.json() == {'username': ['This field is required.']}

    def test_user_create_without_password(self, client) -> None:
        data = {"username": "test_username"}
        response = client.post(self.url, data=data)

        assert response.status_code == 400
        assert response.json() == {'password': ['This field is required.'],
                                   'password_repeat': ['This field is required.']}

    def test_user_create_without_password_repeat(self, client) -> None:
        data = {"username": "test_username",
                "password": "test_password"}
        response = client.post(self.url, data=data)

        assert response.status_code == 400
        assert response.json() == {'password_repeat': ['This field is required.']}

    def test_user_create_with_shot_password(self, client) -> None:

        data = {"username": "test_username",
                "password": "test",
                "password_repeat": "test"}
        response = client.post(self.url, data=data)

        assert response.status_code == 400
        assert response.json() == {'non_field_errors': ['This password is too short. '
                                                        'It must contain at least 8 characters.',
                                                        'This password is too common.']}

    def test_user_create_with_exist_username(self, client) -> None:

        data = {"username": "test_username",
                "password": "test_password",
                "password_repeat": "test_password"}
        client.post(self.url, data=data)
        response = client.post(self.url, data=data)

        assert response.status_code == 400
        assert response.json() == {'username': ['A user with that username already exists.']}


def _serializer_response(user: User, **kwargs) -> dict:
    """
    The _serializer_response function takes as parameters an object of the User class and other named arguments.
    It is a serializer for representing an object of the User class in the form of a dictionary, where the names
    of fields in the form of strings act as keys, and the values of these fields act as values.
    Returns a dictionary compiled from the received instance of the class.
    """
    data: Dict[str, Any] = {'id': user.id,
                            'username': user.username,
                            'first_name': user.first_name,
                            'last_name': user.last_name,
                            'email': user.email,
                            }
    return data | kwargs
