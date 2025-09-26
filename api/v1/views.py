from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from employees.models import Employee, Region
from .serializers import EmployeeSerializer, RegionSerializer
from .permissions import IsAdminOrManager


class RegionViewSet(viewsets.ModelViewSet):
    """CRUD для регионов (доступ только admin/manager)."""
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = [IsAdminOrManager]


class EmployeeViewSet(viewsets.ModelViewSet):
    """CRUD для сотрудников с поиском и фильтрацией."""
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAdminOrManager]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['region', 'position']
    search_fields = ['first_name', 'last_name']
