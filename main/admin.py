from typing import Tuple
from django.contrib import admin

from main.models import Habit


class HabitAdmin(admin.ModelAdmin):
    """
    The HabitAdmin class inherits from the ModelAdmin class. Defines the output of instance fields
    to the administration panel and the ability to edit them.
    """
    list_display: Tuple[str, ...] = ('id', 'title', 'creator', 'time', 'is_pleasant', 'is_public')
    list_filter: Tuple[str, ...] = ('title', )


admin.site.register(Habit, HabitAdmin)
