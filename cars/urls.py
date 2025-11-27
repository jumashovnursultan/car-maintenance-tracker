from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, CarViewSet, ServiceViewSet, RepairViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('cars', CarViewSet, basename='car')
router.register('services', ServiceViewSet, basename='service')
router.register('repairs', RepairViewSet, basename='repair')

urlpatterns = [
    path('', include(router.urls)),
]