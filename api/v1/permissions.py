from rest_framework import permissions


class IsAdminOrManager(permissions.BasePermission):
    """Доступ разрешён только администраторам и менеджерам."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (request.user.is_admin() or request.user.is_manager())
        )
