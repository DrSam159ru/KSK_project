from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def role_required(*allowed_roles):
    """
    Декоратор для проверки роли пользователя.

    Args:
        *allowed_roles (str): список допустимых ролей.

    Raises:
        PermissionDenied: если у пользователя нет атрибута role
        или роль не входит в список разрешённых.

    Returns:
        function: обёрнутая view-функция.

    Пример:
        @role_required("admin", "manager")
        def my_view(request):
            ...
    """

    def decorator(view_func):
        @login_required
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not hasattr(request.user, 'role'):
                raise PermissionDenied('У пользователя нет роли')

            if request.user.role not in allowed_roles:
                raise PermissionDenied(
                    'У вас нет прав для этого действия'
                )

            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator
