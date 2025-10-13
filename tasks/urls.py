from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, StatusViewSet, CategoryViewSet, LogTaskViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'status', StatusViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'logs', LogTaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
