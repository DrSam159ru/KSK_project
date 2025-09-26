from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User
from .models import (
    ActionLog,
    Employee,
    LoginHistory,
    PasswordPolicy,
    Region,
)


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    """Админка для модели Region."""

    list_display = ('code', 'name')
    search_fields = ('code', 'name')
    ordering = ('code',)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    """Админка для модели Employee."""

    list_display = (
        'last_name',
        'first_name',
        'patronymic',
        'region_name',
        'region_code',
        'login',
        'action',
        'status',
        'created_at',
    )
    list_filter = ('region_name', 'action', 'status')
    search_fields = (
        'last_name',
        'first_name',
        'patronymic',
        'login',
        'note_number',
    )
    ordering = ('last_name',)
    readonly_fields = ('created_at',)

    fieldsets = (
        (
            'Личные данные',
            {'fields': ('last_name', 'first_name', 'patronymic')},
        ),
        ('Регион', {'fields': ('region_name', 'region_code')}),
        (
            'Служебная записка',
            {'fields': ('note_date', 'note_number', 'action')},
        ),
        (
            'Учётные данные',
            {'fields': ('login', 'password', 'status', 'created_at')},
        ),
    )


@admin.register(PasswordPolicy)
class PasswordPolicyAdmin(admin.ModelAdmin):
    """Админка для политики паролей (Singleton)."""

    list_display = ("__str__",)
    fields = ("uppercase", "lowercase", "digits", "symbols", "allowed_symbols")

    def has_add_permission(self, request):
        """Запрещаем добавление второй политики."""
        if PasswordPolicy.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        """Запрещаем удаление политики."""
        return False


@admin.register(ActionLog)
class ActionLogAdmin(admin.ModelAdmin):
    """Админка для модели ActionLog."""

    list_display = ('timestamp', 'user', 'action', 'employee', 'ip')
    list_filter = ('action', 'timestamp')
    search_fields = ('user__username', 'employee', 'ip', 'user_agent')
    ordering = ('-timestamp',)
    readonly_fields = ('timestamp',)

    def has_add_permission(self, request):
        """Запрещает ручное добавление записей."""
        return False

    def has_change_permission(self, request, obj=None):
        """Запрещает изменение существующих записей."""
        return False


@admin.register(LoginHistory)
class LoginHistoryAdmin(admin.ModelAdmin):
    """Админка для модели LoginHistory."""

    list_display = ('timestamp', 'user', 'username', 'success', 'ip')
    list_filter = ('success', 'timestamp')
    search_fields = ('user__username', 'username', 'ip', 'user_agent')
    ordering = ('-timestamp',)
    readonly_fields = ('timestamp',)

    def has_add_permission(self, request):
        """Запрещает ручное добавление записей."""
        return False

    def has_change_permission(self, request, obj=None):
        """Запрещает изменение существующих записей."""
        return False


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Админка для кастомной модели User с дополнительным полем role."""

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role',)}),
    )

    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'role',
        'is_staff',
    )
    list_filter = ('role', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'first_name', 'last_name')
