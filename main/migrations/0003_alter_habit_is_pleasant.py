# Generated by Django 4.2.4 on 2023-08-30 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_habit_options_habit_action_habit_creator_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habit',
            name='is_pleasant',
            field=models.BooleanField(default=False, verbose_name='признак полезной привычки'),
        ),
    ]
