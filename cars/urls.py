from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, CarViewSet, ServiceViewSet, RepairViewSet,
    home, login_view, register_view, logout_view, 
    cars_list_view, repairs_list_view
)

# API Router
router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('cars', CarViewSet, basename='car')
router.register('services', ServiceViewSet, basename='service')
router.register('repairs', RepairViewSet, basename='repair')

urlpatterns = [
    # API endpoints
    path('api/', include(router.urls)),
    
    # Frontend страницы
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('cars/', cars_list_view, name='cars_list'),
    path('repairs/', repairs_list_view, name='repairs_list'),
]