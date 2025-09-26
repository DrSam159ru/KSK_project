import logging

from rest_framework import permissions, viewsets

from .models import Employee, Region
from .serializers import EmployeeSerializer, RegionSerializer

logger = logging.getLogger(__name__)


class EmployeeViewSet(viewsets.ModelViewSet):
    """ViewSet для управления сотрудниками через API."""

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Сохраняет нового сотрудника и пишет информацию в лог.

        Args:
            serializer (EmployeeSerializer): сериализатор с данными
            сотрудника.
        """
        employee = serializer.save()
        logger.info("Создан сотрудник через API: %s", employee)


class RegionViewSet(viewsets.ModelViewSet):
    """ViewSet для управления регионами через API."""

    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Сохраняет новый регион и пишет информацию в лог.

        Args:
            serializer (RegionSerializer): сериализатор с данными региона.
        """
        region = serializer.save()
        logger.info("Добавлен регион через API: %s", region)
