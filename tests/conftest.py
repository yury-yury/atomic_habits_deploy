from pytest_factoryboy import register

from tests.factories import UserFactory, HabitFactory


pytest_plugins = 'tests.fixtures'

register(UserFactory)
register(HabitFactory)
