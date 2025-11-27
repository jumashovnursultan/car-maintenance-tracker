from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone


class Car(models.Model):
    """Модель автомобиля"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cars')
    brand = models.CharField(max_length=100, verbose_name='Марка')
    model = models.CharField(max_length=100, verbose_name='Модель')
    year = models.IntegerField(verbose_name='Год выпуска')
    mileage = models.IntegerField(verbose_name='Пробег (км)')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"


class Service(models.Model):
    """Модель сервиса/СТО"""
    name = models.CharField(max_length=200, verbose_name='Название сервиса')
    address = models.CharField(max_length=300, verbose_name='Адрес', blank=True)
    phone = models.CharField(max_length=20, verbose_name='Телефон', blank=True)

    class Meta:
        verbose_name = 'Сервис'
        verbose_name_plural = 'Сервисы'

    def __str__(self):
        return self.name


class Repair(models.Model):
    """Модель ремонта"""
    REPAIR_TYPES = [
        ('maintenance', 'Техническое обслуживание'),
        ('repair', 'Ремонт'),
        ('replacement', 'Замена деталей'),
        ('diagnostics', 'Диагностика'),
    ]

    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='repairs')
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    repair_type = models.CharField(max_length=20, choices=REPAIR_TYPES, verbose_name='Тип работы')
    description = models.TextField(verbose_name='Описание работ')
    date = models.DateField(verbose_name='Дата ремонта')
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Стоимость')
    mileage_at_repair = models.IntegerField(verbose_name='Пробег на момент ремонта')
    next_maintenance_date = models.DateField(null=True, blank=True, verbose_name='Дата следующего ТО')
    next_maintenance_mileage = models.IntegerField(null=True, blank=True, verbose_name='Пробег следующего ТО')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Ремонт'
        verbose_name_plural = 'Ремонты'
        ordering = ['-date']

    def __str__(self):
        return f"{self.car} - {self.get_repair_type_display()} ({self.date})"

    def save(self, *args, **kwargs):
        # Автоматический расчёт следующего ТО (через 6 месяцев и +10000 км)
        if not self.next_maintenance_date:
            self.next_maintenance_date = self.date + timedelta(days=180)
        if not self.next_maintenance_mileage:
            self.next_maintenance_mileage = self.mileage_at_repair + 10000
        super().save(*args, **kwargs)

    def needs_maintenance(self):
        """Проверка, нужно ли ТО"""
        today = timezone.now().date()
        if self.next_maintenance_date and today >= self.next_maintenance_date:
            return True
        if self.next_maintenance_mileage and self.car.mileage >= self.next_maintenance_mileage:
            return True
        return False