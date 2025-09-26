from rest_framework import serializers

from employees.models import Employee, Region, PasswordPolicy


class RegionSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Region."""

    class Meta:
        model = Region
        fields = ["id", "code", "name"]


class PasswordPolicySerializer(serializers.ModelSerializer):
    """Сериализатор для модели PasswordPolicy."""

    class Meta:
        model = PasswordPolicy
        fields = "__all__"


class EmployeeReadSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения сотрудников (с вложенными регионами)."""

    region_name = RegionSerializer(read_only=True)
    region_code = RegionSerializer(read_only=True)

    class Meta:
        model = Employee
        fields = [
            "id",
            "last_name",
            "first_name",
            "patronymic",
            "region_name",
            "region_code",
            "status",
            "created_at",
            "updated_at",
        ]


class EmployeeWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для записи сотрудников (через id регионов)."""

    class Meta:
        model = Employee
        fields = [
            "id",
            "last_name",
            "first_name",
            "patronymic",
            "region_name",
            "region_code",
            "status",
        ]
