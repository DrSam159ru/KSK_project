from rest_framework import permissions


class IsAdminOrManager(permissions.BasePermission):
    """
    Админ — полный доступ.
    Менеджер — может управлять сотрудниками (CRUD).
    Просмотрщик — только GET-запросы.
    """

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        if user.is_admin():
            return True

        if user.is_manager():
            return True

        if user.is_viewer() and request.method in permissions.SAFE_METHODS:
            return True

        return False
