from typing import Dict

from django.contrib.auth.models import AbstractUser
from django.db import models


NULLABLE: Dict[str, bool] = {'null': True, 'blank': True}


class User(AbstractUser):
    """
    The User class is an inheritor of the AbstractUser class from the django.contrib.auth.models library.
    This is the data model contained in the user database table.
    """
    chat_id = models.CharField(max_length=15, verbose_name='ID TG', **NULLABLE)
