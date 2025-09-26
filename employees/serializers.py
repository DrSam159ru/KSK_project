from rest_framework import serializers

from .models import Employee, Region


class RegionSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Region."""

    class Meta:
        model = Region
        fields = ['id', 'name', 'code']


class EmployeeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Employee."""

    region_name = serializers.StringRelatedField()
    region_code = serializers.StringRelatedField()
    status = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Employee
        fields = [
            'id',
            'last_name',
            'first_name',
            'patronymic',
            'region_name',
            'region_code',
            'note_date',
            'note_number',
            'login',
            'password',
            'action',
            'status',
            'created_at',
        ]
