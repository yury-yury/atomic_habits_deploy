from typing import List
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from main.models import Habit
from main.serializers import HabitSerializer
from main.services import create_habit_schedule


class HabitsViewSet(viewsets.ModelViewSet):
    """
    The HabitsViewSet class inherits from the ModelViewSet base class from the rest_framework.viewsets module.
    Defines a complete set of CRUD endpoints for working with instances of the Habit class.
    """
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer) -> None:
        """
        The perform_create function overrides the parent class method.
        Sets the value of the creator field and adds an instance to the schedule for sending a reminder.
        """
        serializer.save(creator=self.request.user)
        habit = serializer.save()
        create_habit_schedule(habit)

    def get_queryset(self) -> List[Habit]:
        """
        The get_queryset function overrides the parent class method. When called, it generates
        a list of instances of the Habit class that satisfy the condition: The user making the request
        must be the creator of the habit. If the current user is superuser,
        then the list will contain all existing instances. Returns the resulting list.
        """
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_superuser:
            return queryset
        else:
            return queryset.filter(creator=user)


class HabitsListView(generics.ListAPIView):
    """
    The HabitsListView class inherits from the ListAPIView class from the rest_framework.generics module.
    Represent a CBV for the "/public_habits/" endpoint that receives a request using the GET method.
    """
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> List[Habit]:
        """
        The get_queryset function overrides the parent class method. When called, it generates
        a list of instances of the Habit class that satisfy the condition:
        an instance of the Habit class must be public. Returns the resulting list.
        """
        return Habit.objects.filter(is_public=True)
