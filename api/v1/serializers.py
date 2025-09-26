from rest_framework import serializers
from employees.models import Employee, Region


class RegionSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Region."""

    class Meta:
        model = Region
        fields = ['id', 'name']


class EmployeeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Employee с поддержкой связанного region."""

    region = RegionSerializer(read_only=True)
    region_id = serializers.PrimaryKeyRelatedField(
        queryset=Region.objects.all(),
        source='region',
        write_only=True
    )

    class Meta:
        model = Employee
        fields = [
            'id', 'first_name', 'last_name', 'position',
            'region', 'region_id', 'hire_date'
        ]
