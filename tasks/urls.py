from django.urls import path
from .views import TaskViewSet, health_check
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('health/', health_check, name='health_check'),
] + router.urls