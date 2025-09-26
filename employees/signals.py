from django.contrib.auth.signals import (
    user_logged_in,
    user_logged_out,
    user_login_failed,
)
from django.dispatch import receiver

from .models import LoginHistory
from .utils import get_client_ip, get_user_agent


@receiver(user_logged_in)
def on_user_logged_in(sender, request, user, **kwargs):
    """
    Сохраняет успешный вход пользователя в LoginHistory.

    Args:
        sender: отправитель сигнала.
        request (HttpRequest): текущий запрос.
        user (User): пользователь, выполнивший вход.
    """
    LoginHistory.objects.create(
        user=user,
        username=user.username,
        success=True,
        ip=get_client_ip(request),
        user_agent=get_user_agent(request),
    )


@receiver(user_logged_out)
def on_user_logged_out(sender, request, user, **kwargs):
    """
    Сохраняет факт выхода пользователя в LoginHistory.

    Args:
        sender: отправитель сигнала.
        request (HttpRequest): текущий запрос.
        user (User): пользователь, выполнивший выход.
    """
    LoginHistory.objects.create(
        user=user,
        username=getattr(user, 'username', ''),
        success=True,
        ip=get_client_ip(request),
        user_agent=get_user_agent(request),
    )


@receiver(user_login_failed)
def on_user_login_failed(sender, credentials, request, **kwargs):
    """
    Сохраняет неудачную попытку входа в LoginHistory.

    Args:
        sender: отправитель сигнала.
        credentials (dict): данные для входа (username, password).
        request (HttpRequest | None): текущий запрос, может быть None.
    """
    username = credentials.get('username') if credentials else ''
    LoginHistory.objects.create(
        user=None,
        username=username or '',
        success=False,
        ip=get_client_ip(request) if request else None,
        user_agent=get_user_agent(request) if request else '',
    )
