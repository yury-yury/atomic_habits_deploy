import datetime
import factory.django

from main.models import Habit
from users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    """
    The UserFactory class is a factory for creating test instances corresponding to the User model in order
    to verify the correct functioning of the application.
    """
    username: str = factory.Faker("user_name")
    password: str = factory.Faker("password")
    email: str = factory.Faker("email")

    class Meta:
        """
        The Meta class contains an indication of the model for creating test instances of objects that replace
        data from the database.
        """
        model = User


class HabitFactory(factory.django.DjangoModelFactory):
    """
    The HabitFactory class is a factory for creating test instances corresponding to the Habit model in order
    to verify the correct functioning of the application.
    """
    title: str = factory.Faker("name")
    creator: User = factory.SubFactory(UserFactory)
    place: str = factory.Faker("name")
    time: datetime.time = factory.Faker("time")

    class Meta:
        """
        The Meta class contains an indication of the model for creating test instances of objects that replace
        data from the database.
        """
        model = Habit
