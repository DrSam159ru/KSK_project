from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from employees.models import Employee, Region, PasswordPolicy
from .serializers import (
    EmployeeReadSerializer,
    EmployeeWriteSerializer,
    RegionSerializer,
    PasswordPolicySerializer,
)
from .permissions import IsAdminOrManager


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    ViewSet для сотрудников.

    - Админ имеет полный доступ.
    - Менеджер может управлять сотрудниками (CRUD).
    - Просмотрщик может только читать.
    """

    queryset = Employee.objects.all()
    permission_classes = [IsAuthenticated, IsAdminOrManager]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # Фильтры
    filterset_fields = ["status", "region_name", "region_code"]
    search_fields = ["last_name", "first_name", "patronymic"]
    ordering_fields = ["last_name", "first_name", "id", "created_at"]

    def get_serializer_class(self):
        """Для чтения используем ReadSerializer, для записи — WriteSerializer."""
        if self.action in ("list", "retrieve"):
            return EmployeeReadSerializer
        return EmployeeWriteSerializer


class RegionViewSet(viewsets.ModelViewSet):
    """ViewSet для регионов."""

    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = [IsAuthenticated, IsAdminOrManager]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name", "code"]
    ordering_fields = ["code", "name"]


class PasswordPolicyViewSet(viewsets.ModelViewSet):
    """ViewSet для политики паролей."""

    queryset = PasswordPolicy.objects.all()
    serializer_class = PasswordPolicySerializer
    permission_classes = [IsAuthenticated, IsAdminOrManager]
