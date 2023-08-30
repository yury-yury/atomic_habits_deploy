from typing import Dict
from django.db import models
from users.models import User


NULLABLE: Dict[str, bool] = {'null': True, 'blank': True}


class Habit(models.Model):
    """
    The Habit class inherits from the Model class. Defines the database table fields
    and their properties.
    """
    title = models.CharField(max_length=150, verbose_name='название')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='создатель', **NULLABLE)
    place = models.CharField(max_length=150, verbose_name='место')
    time = models.TimeField(verbose_name='время')
    action = models.CharField(max_length=150, verbose_name='действие')
    is_pleasant = models.BooleanField(default=False, verbose_name='признак полезной привычки')
    related_habit = models.ForeignKey('self', on_delete=models.SET_NULL, **NULLABLE,
                                      verbose_name='связанная привычка')
    periodicity = models.IntegerField(default=1, verbose_name='периодичность в днях')
    reward = models.CharField(max_length=150, verbose_name='вознаграждение', **NULLABLE)
    execution_time = models.TimeField(verbose_name='время на выполнение', **NULLABLE)
    is_public = models.BooleanField(default=True, verbose_name='признак публичности')

    def __str__(self) -> str:
        """
        The __str__ function overrides the method of the parent class and takes no arguments except for an instance
        of its own class. When called, returns a human-readable representation of the class instance as a string.
        """
        return f'{self.title}'

    class Meta:
        """
        The Meta class contains the common name of the model instance in the singular and plural used
        in the administration panel.
        """
        verbose_name: str = 'Привычка'
        verbose_name_plural: str = 'Привычки'
