from rest_framework import serializers

from main.models import Habit
from main.validators import habit_validators


class HabitSerializer(serializers.ModelSerializer):
    """
    The HabitSerializer class inherits from the ModelSerializer class from rest_framework.serializers.
    This is a class for convenient serialization and deserialization of objects of the Habit.
    """
    class Meta:
        """
        The Meta class is an internal service class of the serializer,
        defines the necessary parameters for the serializer to function.
        """
        model = Habit
        fields = "__all__"
        validators = [habit_validators, ]
