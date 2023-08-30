from rest_framework.routers import DefaultRouter
from django.urls import path

from main.views import HabitsViewSet, HabitsListView

router = DefaultRouter()
router.register('habits', HabitsViewSet, basename='habits')


urlpatterns = [
    path('public_habits/', HabitsListView.as_view(), name='habits_list'),
              ] + router.urls
