from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Car, Service, Repair
from .serializers import UserSerializer, CarSerializer, ServiceSerializer, RepairSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """API для просмотра пользователей"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class CarViewSet(viewsets.ModelViewSet):
    """API для управления автомобилями"""
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Показываем только машины текущего пользователя
        return Car.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        # Автоматически привязываем машину к текущему пользователю
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['get'])
    def repairs(self, request, pk=None):
        """Получить все ремонты конкретной машины"""
        car = self.get_object()
        repairs = car.repairs.all()
        serializer = RepairSerializer(repairs, many=True)
        return Response(serializer.data)


class ServiceViewSet(viewsets.ModelViewSet):
    """API для управления сервисами"""
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated]


class RepairViewSet(viewsets.ModelViewSet):
    """API для управления ремонтами"""
    serializer_class = RepairSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Показываем только ремонты машин текущего пользователя
        return Repair.objects.filter(car__user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def needs_maintenance(self, request):
        """Получить список ремонтов, требующих ТО"""
        repairs = self.get_queryset()
        repairs_needing_maintenance = [r for r in repairs if r.needs_maintenance()]
        serializer = self.get_serializer(repairs_needing_maintenance, many=True)
        return Response(serializer.data)



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages


# Страницы для фронтенда
def home(request):
    """Главная страница"""
    return render(request, 'cars/home.html')


def login_view(request):
    """Страница логина"""
    if request.user.is_authenticated:
        return redirect('cars_list')
    
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('cars_list')
    else:
        form = AuthenticationForm()
    
    return render(request, 'cars/login.html', {'form': form})


def register_view(request):
    """Страница регистрации"""
    if request.user.is_authenticated:
        return redirect('cars_list')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация успешна!')
            return redirect('cars_list')
    else:
        form = UserCreationForm()
    
    return render(request, 'cars/register.html', {'form': form})


def logout_view(request):
    """Выход"""
    logout(request)
    return redirect('login')


@login_required
def cars_list_view(request):
    """Страница списка машин"""
    return render(request, 'cars/cars_list.html')


@login_required
def repairs_list_view(request):
    """Страница списка ремонтов"""
    return render(request, 'cars/repairs_list.html')        