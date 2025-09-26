from django.apps import AppConfig


class EmployeesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'employees'
    verbose_name = "Сотрудники"

    def ready(self):
        # подключаем сигналы
        from . import signals  # noqa: F401
