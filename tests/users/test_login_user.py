import pytest

from users.models import User
from users.serializers import LoginSerializer


@pytest.mark.django_db
class TestUserCreate:
    url: str = '/user/login'

    def test_user_login(self, client) -> None:
        data = {"username": "test_username",
                "password": "test_password",
                "password_repeat": "test_password"}
        client.post('/user/signup', data=data)

        data = {"username": "test_username",
                "password": "test_password"}
        response = client.post(self.url, data=data)

        new_user = User.objects.get()

        assert response.status_code == 200
        assert response.json() == LoginSerializer(new_user).data
        assert new_user.is_authenticated

    def test_user_login_without_data(self, client) -> None:
        response = client.post(self.url, data={})

        assert response.status_code == 400
        assert response.json() == {
            'password': ['This field is required.'],
            'username': ['This field is required.']
        }
