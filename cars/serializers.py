from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Car, Service, Repair


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class CarSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Car
        fields = ['id', 'user', 'brand', 'model', 'year', 'mileage', 'created_at']
        read_only_fields = ['created_at', 'user']


class RepairSerializer(serializers.ModelSerializer):
    car = CarSerializer(read_only=True)
    car_id = serializers.IntegerField(write_only=True)
    service = ServiceSerializer(read_only=True)
    service_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    needs_maintenance = serializers.SerializerMethodField()
    
    class Meta:
        model = Repair
        fields = [
            'id', 'car', 'car_id', 'service', 'service_id', 
            'repair_type', 'description', 'date', 'cost', 
            'mileage_at_repair', 'next_maintenance_date', 
            'next_maintenance_mileage', 'needs_maintenance', 'created_at'
        ]
        read_only_fields = ['created_at', 'next_maintenance_date', 'next_maintenance_mileage']
    
    def get_needs_maintenance(self, obj):
        return obj.needs_maintenance()