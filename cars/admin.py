from django.contrib import admin
from .models import Car, Service, Repair


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['brand', 'model', 'year', 'mileage', 'user', 'created_at']
    list_filter = ['brand', 'year', 'user']
    search_fields = ['brand', 'model']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'phone']
    search_fields = ['name', 'address']


@admin.register(Repair)
class RepairAdmin(admin.ModelAdmin):
    list_display = ['car', 'repair_type', 'date', 'cost', 'mileage_at_repair', 'needs_maintenance']
    list_filter = ['repair_type', 'date', 'car']
    search_fields = ['description', 'car__brand', 'car__model']
    date_hierarchy = 'date'
    
    def needs_maintenance(self, obj):
        return obj.needs_maintenance()
    needs_maintenance.boolean = True
    needs_maintenance.short_description = 'Требует ТО'