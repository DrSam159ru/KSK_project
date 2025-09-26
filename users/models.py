from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Кастомная модель пользователя с ролями."""

    class Roles(models.TextChoices):
        """Возможные роли пользователей."""

        ADMIN = 'admin', 'Администратор'
        MANAGER = 'staff', 'Персонал'
        VIEWER = 'user', 'Пользователь'

    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.VIEWER,
        verbose_name='Роль',
    )

    def is_admin(self) -> bool:
        """
        Проверяет, является ли пользователь администратором.

        Returns:
            bool: True, если роль admin или is_superuser.
        """
        return self.role == self.Roles.ADMIN or self.is_superuser

    def is_manager(self) -> bool:
        """
        Проверяет, является ли пользователь менеджером.

        Returns:
            bool: True, если роль manager.
        """
        return self.role == self.Roles.MANAGER

    def is_viewer(self) -> bool:
        """
        Проверяет, является ли пользователь просмотрщиком.

        Returns:
            bool: True, если роль viewer.
        """
        return self.role == self.Roles.VIEWER

    def __str__(self) -> str:
        """Строковое представление пользователя."""
        return f'{self.username} ({self.role})'
