import re

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone


def validate_allowed_symbols(value):
    """Разрешаем только ASCII-символы без пробелов и кириллицы."""
    if re.search(r"\s", value):
        raise ValidationError("Нельзя использовать пробелы в символах.")
    if re.search(r"[А-Яа-яЁё]", value):
        raise ValidationError("Нельзя использовать кириллицу.")
    if not re.match(r"^[!-~]+$", value):  # ASCII печатные символы
        raise ValidationError("Допустимы только ASCII-символы (без пробелов).")


def validate_not_future(value):
    """Запрещает использовать даты из будущего."""
    if value and value > timezone.localdate():
        raise ValidationError("Дата не может быть из будущего.")


class Region(models.Model):
    """Регион, используется для привязки сотрудников."""

    name = models.CharField(
        max_length=150,
        verbose_name="Регион (код и название)",
    )
    code = models.CharField(
        max_length=2,
        unique=True,
        verbose_name="Код региона",
        validators=[
            RegexValidator(
                r"^\d{2}$",
                "Код региона должен быть двухзначным",
            )
        ],
    )

    class Meta:
        verbose_name = "Регион"
        verbose_name_plural = "Регионы"

    def __str__(self):
        return f"{self.code} – {self.name}"


class PasswordPolicy(models.Model):
    """Модель описывает правила формирования пароля."""

    uppercase = models.PositiveIntegerField(
        default=1,
        verbose_name="Кол-во заглавных",
    )
    lowercase = models.PositiveIntegerField(
        default=1,
        verbose_name="Кол-во строчных",
    )
    digits = models.PositiveIntegerField(
        default=1,
        verbose_name="Кол-во цифр",
    )
    symbols = models.PositiveIntegerField(
        default=1,
        verbose_name="Кол-во символов",
    )
    allowed_symbols = models.CharField(
        max_length=100,
        default="!@#$%^&*()-_=+<>?",
        verbose_name="Разрешённые спецсимволы",
        validators=[validate_allowed_symbols],
        help_text="Только ASCII-символы, без пробелов и кириллицы.",
    )

    class Meta:
        verbose_name = "Политика паролей"
        verbose_name_plural = "Политика паролей"

    def __str__(self):
        return (
            f"A:{self.uppercase} a:{self.lowercase} "
            f"0:{self.digits} sym:{self.symbols} [{self.allowed_symbols}]"
        )


class Employee(models.Model):
    """Сотрудник организации."""

    ACTIONS = [
        ("create", "Создание"),
        ("block", "Блокировка"),
    ]

    STATUSES = [
        ("active", "Работает"),
        ("blocked", "Заблокирован"),
    ]

    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    patronymic = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Отчество",
    )

    region_name = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        related_name="as_name",
        verbose_name="Регион",
    )
    region_code = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        related_name="as_code",
        verbose_name="Код региона",
    )

    note_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Дата служебной записки",
        validators=[validate_not_future],
    )
    note_number = models.CharField(
        max_length=50,
        verbose_name="Номер служебной записки",
    )

    login = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Логин",
    )
    password = models.CharField(
        max_length=128,
        verbose_name="Пароль (хранится открытым текстом по ТЗ)",
    )
    action = models.CharField(
        max_length=10,
        choices=ACTIONS,
        default="create",
        verbose_name="Действие",
    )

    status = models.CharField(
        max_length=10,
        choices=STATUSES,
        default="active",
        verbose_name="Статус",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    def __str__(self):
        return (
            f"{self.last_name} {self.first_name} "
            f"({self.region_code.code}) – {self.get_status_display()}"
        )


class ActionLog(models.Model):
    """Лог действий пользователей над сотрудниками."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Пользователь",
    )
    action = models.CharField(max_length=100, verbose_name="Действие")
    employee = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Сотрудник",
    )
    ip = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name="IP",
    )
    user_agent = models.CharField(
        max_length=300,
        null=True,
        blank=True,
        verbose_name="User-Agent",
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Время",
    )

    class Meta:
        ordering = ("-timestamp",)
        verbose_name = "Лог действия"
        verbose_name_plural = "Логи действий"

    def __str__(self):
        return f"[{self.timestamp}] {self.user} {self.action} {self.employee}"


class LoginHistory(models.Model):
    """История входов пользователей в систему."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Пользователь",
    )
    username = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Имя учётки (если неизвестен пользователь)",
    )
    success = models.BooleanField(default=False, verbose_name="Успех")
    ip = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name="IP",
    )
    user_agent = models.TextField(
        null=True,
        blank=True,
        verbose_name="User-Agent",
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Время",
    )

    class Meta:
        ordering = ("-timestamp",)
        verbose_name = "История входов"
        verbose_name_plural = "История входов"

    def __str__(self):
        user_display = self.user or self.username or "unknown"
        status = "ok" if self.success else "fail"
        return f"[{self.timestamp}] login {status}: {user_display}"
