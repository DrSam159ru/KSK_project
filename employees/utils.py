import random
import string
from typing import Optional

from .models import ActionLog, PasswordPolicy


import random
import string

from .models import PasswordPolicy


def generate_password() -> str:
    """
    Генерирует пароль на основе политики PasswordPolicy.

    Если политика отсутствует — создаётся со значениями по умолчанию.
    """
    policy = PasswordPolicy.objects.first()
    if not policy:
        policy = PasswordPolicy.objects.create()

    chars = []
    chars.extend(random.choices(string.ascii_uppercase, k=policy.uppercase))
    chars.extend(random.choices(string.ascii_lowercase, k=policy.lowercase))
    chars.extend(random.choices(string.digits, k=policy.digits))

    # ✅ используем символы, которые задал админ
    if policy.allowed_symbols:
        chars.extend(random.choices(policy.allowed_symbols, k=policy.symbols))

    random.shuffle(chars)
    return ''.join(chars)


def get_client_ip(request) -> Optional[str]:
    """
    Извлекает IP-адрес клиента из объекта запроса.

    Args:
        request (HttpRequest): объект запроса.

    Returns:
        str | None: IP-адрес клиента или None.
    """
    xfwd = request.META.get('HTTP_X_FORWARDED_FOR')
    if xfwd:
        return xfwd.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def get_user_agent(request) -> str:
    """
    Возвращает строку User-Agent из заголовков запроса.

    Args:
        request (HttpRequest): объект запроса.

    Returns:
        str: строка User-Agent (не более 300 символов).
    """
    return request.META.get('HTTP_USER_AGENT', '')[:300]


def employee_to_str(employee) -> str:
    """
    Преобразует объект сотрудника в строку формата:
    "Фамилия Имя [Отчество] (логин)".

    Args:
        employee (Employee | None): сотрудник.

    Returns:
        str: строковое представление сотрудника.
    """
    if not employee:
        return ''
    fio = f'{employee.last_name} {employee.first_name}'
    if employee.patronymic:
        fio += f' {employee.patronymic}'
    return f'{fio} ({employee.login})'


def log_action(
    request,
    action: str,
    employee: Optional[object] = None,
    extra_employee_text: str = '',
) -> None:
    """
    Добавляет запись в ActionLog.

    Args:
        request (HttpRequest): текущий запрос.
        action (str): действие пользователя.
        employee (Employee | None, optional): объект сотрудника.
        extra_employee_text (str, optional): дополнительный текст,
            если сотрудник не передан.

    Returns:
        None
    """
    ActionLog.objects.create(
        user=(
            request.user
            if getattr(request, 'user', None)
            and request.user.is_authenticated
            else None
        ),
        action=action,
        employee=employee_to_str(employee) or extra_employee_text,
        ip=get_client_ip(request),
        user_agent=get_user_agent(request),
    )
