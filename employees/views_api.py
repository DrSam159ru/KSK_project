from rest_framework import permissions, viewsets

from .models import Employee, Region
from .serializers import EmployeeSerializer, RegionSerializer
from .utils import log_action


class IsAdminOrManager(permissions.BasePermission):
    """Разрешение для пользователей с ролью admin или manager."""

    def has_permission(self, request, view):
        """
        Проверяет, что пользователь аутентифицирован
        и имеет роль admin или manager.
        """
        user = request.user
        return user.is_authenticated and getattr(
            user, 'role', ''
        ) in ('admin', 'manager')


class EmployeeViewSet(viewsets.ModelViewSet):
    """ViewSet для сотрудников (CRUD через API)."""

    queryset = Employee.objects.all().select_related('region_name', 'region_code')
    serializer_class = EmployeeSerializer

    def get_permissions(self):
        """
        Ограничивает доступ:
        - list/retrieve: только аутентифицированные пользователи.
        - create/update/delete: только admin или manager.
        """
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [IsAdminOrManager()]

    def perform_create(self, serializer):
        """Создание сотрудника через API + логирование действия."""
        employee = serializer.save()
        log_action(self.request, 'api_create_employee', employee)

    def perform_update(self, serializer):
        """Обновление сотрудника через API + логирование действия."""
        employee = serializer.save()
        log_action(self.request, 'api_update_employee', employee)

    def perform_destroy(self, instance):
        """Удаление сотрудника через API + логирование действия."""
        log_action(self.request, 'api_delete_employee', instance)
        instance.delete()


class RegionViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для списка регионов (только чтение)."""

    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = [permissions.IsAuthenticated]
