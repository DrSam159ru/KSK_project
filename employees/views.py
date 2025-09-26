import logging
from urllib.parse import urlencode

from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from openpyxl import Workbook

from .forms import EmployeeForm, SearchForm
from .models import ActionLog, Employee, Region
from .utils import generate_password

# Логгеры
app_logger = logging.getLogger('app')
actions_logger = logging.getLogger('actions')
employees_logger = logging.getLogger('employees')


# =====================
# 🔹 Авторизация
# =====================
def user_login(request):
    """Авторизация пользователя."""

    # очищаем старые сообщения
    storage = messages.get_messages(request)
    storage.used = True

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            app_logger.info("Вход: %s", user.username)
            return redirect('index')

        messages.error(request, 'Неверный логин или пароль')
        employees_logger.warning("Неудачная попытка входа: %s", username)
        return redirect('login')

    return render(request, 'login.html')


@login_required
def user_logout(request):
    """Выход пользователя из системы."""
    username = request.user.username
    logout(request)

    # очистка старых сообщений
    storage = messages.get_messages(request)
    storage.used = True

    messages.info(request, 'Вы вышли из системы.')
    app_logger.info("Выход: %s", username)
    return redirect('login')


@login_required
def index(request):
    """Главная страница (доступна только авторизованным)."""
    return render(request, 'index.html')


# =====================
# 🔹 Создание сотрудника
# =====================
@login_required
def create_employee(request):
    """Создание нового сотрудника (admin и manager)."""

    # очищаем сообщения от предыдущих действий
    storage = messages.get_messages(request)
    storage.used = True

    if not (request.user.is_admin or request.user.is_manager):
        messages.error(request, 'У вас нет прав для создания сотрудников.')
        return redirect('search_employee')

    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            last_name = form.cleaned_data['last_name'].capitalize()
            first_name = form.cleaned_data['first_name'].capitalize()
            patronymic = (
                form.cleaned_data['patronymic'].capitalize()
                if form.cleaned_data['patronymic']
                else ''
            )
            region_name = form.cleaned_data['region_name']
            note_date = form.cleaned_data['note_date']
            note_number = form.cleaned_data['note_number']

            login_value = (
                f"{region_name.code}_{last_name}_"
                f"{first_name[0].upper()}"
                f"{patronymic[0].upper() if patronymic else ''}"
            )
            password_value = generate_password()

            existing = Employee.objects.filter(
                last_name=last_name,
                first_name=first_name,
                patronymic=patronymic,
                region_name=region_name,
            ).first()

            if existing:
                messages.warning(
                    request,
                    f'Сотрудник {last_name} {first_name} {patronymic} '
                    f'в регионе {region_name} уже существует.',
                )
            else:
                emp = Employee.objects.create(
                    last_name=last_name,
                    first_name=first_name,
                    patronymic=patronymic,
                    region_name=region_name,
                    region_code=region_name,
                    note_date=note_date,
                    note_number=note_number,
                    login=login_value,
                    password=password_value,
                    action='create',
                )
                messages.success(request, f'Сотрудник {emp} успешно создан!')
                actions_logger.info("%s создал сотрудника %s", request.user, emp)
                ActionLog.objects.create(
                    user=request.user, action='Создание', employee=str(emp)
                )
                return redirect('create_employee')
    else:
        form = EmployeeForm()

    return render(request, 'create_employee.html', {'form': form})


# =====================
# 🔹 Редактирование
# =====================
@login_required
def edit_employee(request, pk):
    """Редактирование сотрудника с подтверждением (admin и manager)."""
    if not (request.user.is_admin or request.user.is_manager):
        messages.error(request, "У вас нет прав для редактирования сотрудников.")
        return redirect("search_employee")

    employee = get_object_or_404(Employee, pk=pk)

    if request.method == "POST":
        # Шаг 2: Подтверждение
        if request.POST.get("confirm") == "yes":
            form_data = request.session.get("edit_data")
            if not form_data:
                messages.error(request, "Нет данных для сохранения.")
                return redirect("search_employee")

            form = EmployeeForm(form_data, instance=employee)
            if form.is_valid():
                emp = form.save(commit=False)
                emp.login = request.session.get("edit_login", emp.login)
                emp.password = request.session.get("edit_password", emp.password)
                emp.save()

                messages.success(request, f"Сотрудник {emp} успешно изменён!")

                # очищаем сессию
                for key in ["edit_data", "edit_login", "edit_password"]:
                    request.session.pop(key, None)

                prev_url = request.POST.get("prev_url") or reverse("search_employee")
                return redirect(prev_url)

        # Шаг 1: Запрос на подтверждение
        else:
            form = EmployeeForm(request.POST, instance=employee)
            if form.is_valid():
                request.session["edit_data"] = request.POST
                request.session["edit_login"] = request.POST.get("login", employee.login)
                request.session["edit_password"] = request.POST.get("password", employee.password)

                prev_url = request.GET.get("prev_url") or request.META.get(
                    "HTTP_REFERER", reverse("search_employee")
                )
                return render(
                    request,
                    "confirm_edit.html",
                    {"employee": employee, "prev_url": prev_url, "saved": False},
                )

    else:
        form = EmployeeForm(instance=employee)

    return render(request, "edit_employee.html", {"form": form, "employee": employee})


# =====================
# 🔹 Удаление
# =====================
@login_required
def delete_employee(request, pk):
    """Удаление сотрудника (только admin)."""
    if not request.user.is_admin:
        messages.error(request, 'Удаление доступно только администраторам.')
        return redirect('search_employee')

    employee = get_object_or_404(Employee, pk=pk)

    if request.method == 'POST':
        if request.POST.get('confirm') == 'yes':
            employee_str = str(employee)
            employee.delete()
            messages.info(request, f'Сотрудник {employee_str} удалён.')
            prev_url = request.POST.get('prev_url') or reverse(
                'search_employee'
            )
            return render(
                request,
                'confirm_delete.html',
                {'employee': employee_str, 'prev_url': prev_url, 'deleted': True},
            )

        prev_url = request.GET.get('prev_url') or request.META.get(
            'HTTP_REFERER', reverse('search_employee')
        )
        return render(
            request,
            'confirm_delete.html',
            {'employee': employee, 'prev_url': prev_url, 'deleted': False},
        )

    return render(request, 'delete_employee.html', {'employee': employee})


# =====================
# 🔹 Поиск сотрудников
# =====================
@login_required
def search_employee(request):
    """Поиск сотрудников по заданным фильтрам."""
    form = SearchForm(request.GET or None)
    employees = Employee.objects.none()

    if form.is_valid():
        qs = Employee.objects.all()
        canon = {}

        last_name = form.cleaned_data.get('last_name')
        first_name = form.cleaned_data.get('first_name')
        patronymic = form.cleaned_data.get('patronymic')
        region_obj = form.cleaned_data.get('region_name')
        note_date = form.cleaned_data.get('note_date')
        note_number = form.cleaned_data.get('note_number')
        status = form.cleaned_data.get('status')
        created_at = form.cleaned_data.get('created_at')

        if last_name:
            qs = qs.filter(last_name__icontains=last_name)
            canon['last_name'] = last_name
        if first_name:
            qs = qs.filter(first_name__icontains=first_name)
            canon['first_name'] = first_name
        if patronymic:
            qs = qs.filter(patronymic__icontains=patronymic)
            canon['patronymic'] = patronymic
        if region_obj:
            qs = qs.filter(region_name=region_obj)
            canon['region_name'] = str(region_obj.id)
        if note_date:
            qs = qs.filter(note_date=note_date)
            canon['note_date'] = note_date.isoformat()
        if note_number:
            qs = qs.filter(note_number__icontains=note_number)
            canon['note_number'] = note_number
        if status:
            qs = qs.filter(status=status)
            canon['status'] = status
        if created_at:
            qs = qs.filter(created_at__date=created_at)
            canon['created_at'] = created_at.isoformat()

        # Канонизация URL
        current = {k: v for k, v in request.GET.items() if v}
        if current != canon:
            return redirect(f"{reverse('search_employee')}?{urlencode(canon)}")

        employees = qs
        if not employees.exists():
            messages.warning(request, 'По вашему запросу ничего не найдено.')

    return render(
        request, 'search_employee.html', {'employees': employees, 'form': form}
    )


# =====================
# 🔹 Подтверждение экспорта
# =====================
@login_required
def confirm_export(request):
    """Подтверждение экспорта сотрудников в Excel."""
    if not (request.user.is_admin or request.user.is_manager):
        messages.error(request, 'Нет прав на экспорт сотрудников.')
        return redirect('search_employee')

    filters = {}
    if request.GET.get('last_name'):
        filters['last_name__icontains'] = request.GET['last_name']
    if request.GET.get('first_name'):
        filters['first_name__icontains'] = request.GET['first_name']
    if request.GET.get('patronymic'):
        filters['patronymic__icontains'] = request.GET['patronymic']
    if request.GET.get('region_name'):
        filters['region_name'] = request.GET['region_name']
    if request.GET.get('region'):  # фильтр по региону через employees_by_region
        filters['region_name_id'] = request.GET['region']
    if request.GET.get('note_date'):
        filters['note_date'] = request.GET['note_date']
    if request.GET.get('note_number'):
        filters['note_number__icontains'] = request.GET['note_number']

    employees = Employee.objects.filter(**filters)
    count = employees.count()

    return render(
        request,
        'confirm_export.html',
        {
            'count': count,
            'query': request.GET.urlencode(),
            'prev_url': request.META.get(
                'HTTP_REFERER', reverse('search_employee')
            ),
        },
    )


# =====================
# 🔹 Экспорт Excel
# =====================
@login_required
def export_excel(request):
    """Экспорт списка сотрудников в Excel."""
    if not (request.user.is_admin or request.user.is_manager):
        messages.error(request, 'Нет прав на экспорт сотрудников.')
        return redirect('search_employee')

    filters = {}
    if request.GET.get('last_name'):
        filters['last_name__icontains'] = request.GET['last_name']
    if request.GET.get('first_name'):
        filters['first_name__icontains'] = request.GET['first_name']
    if request.GET.get('patronymic'):
        filters['patronymic__icontains'] = request.GET['patronymic']
    if request.GET.get('region_name'):
        filters['region_name'] = request.GET['region_name']
    if request.GET.get('region'):  # фильтр по региону через employees_by_region
        filters['region_name_id'] = request.GET['region']
    if request.GET.get('note_date'):
        filters['note_date'] = request.GET['note_date']
    if request.GET.get('note_number'):
        filters['note_number__icontains'] = request.GET['note_number']

    employees = Employee.objects.filter(**filters)

    if not employees.exists():
        messages.warning(request, 'Нет сотрудников для экспорта.')
        return redirect(
            request.META.get('HTTP_REFERER', reverse('search_employee'))
        )

    # 📊 Формируем Excel
    wb = Workbook()
    ws = wb.active
    ws.title = 'Сотрудники'
    ws.append(
        [
            'Фамилия',
            'Имя',
            'Отчество',
            'Регион',
            'Дата записки',
            'Номер записки',
            'Логин',
            'Пароль',
        ]
    )

    for emp in employees:
        ws.append(
            [
                emp.last_name,
                emp.first_name,
                emp.patronymic or '',
                emp.region_name.name,
                emp.note_date or '',
                emp.note_number,
                emp.login,
                emp.password,
            ]
        )

    response = HttpResponse(
        content_type=(
            'application/vnd.openxmlformats-'
            'officedocument.spreadsheetml.sheet'
        )
    )
    response['Content-Disposition'] = 'attachment; filename="employees.xlsx"'
    wb.save(response)
    return response


# =====================
# 🔹 Генерация пароля
# =====================
@login_required
def generate_password_view(request):
    """Возвращает сгенерированный пароль в JSON-ответе."""
    return JsonResponse({'password': generate_password()})


# =====================
# 🔹 Справка и ошибки
# =====================
def help(request):
    """Страница справки."""
    return render(request, 'help.html')


def error_403(request, exception=None):
    """Обработчик ошибки 403 (доступ запрещён)."""
    user = request.user if request.user.is_authenticated else 'Аноним'
    employees_logger.warning(
        "Ошибка 403: доступ запрещён. Пользователь: %s", user
    )
    return render(request, '403.html', status=403)


def error_404(request, exception=None):
    """Обработчик ошибки 404 (страница не найдена)."""
    user = request.user if request.user.is_authenticated else 'Аноним'
    path = request.path
    employees_logger.error("Ошибка 404: %s. Пользователь: %s", path, user)
    return render(request, '404.html', status=404)


def error_500(request):
    """Обработчик ошибки 500 (внутренняя ошибка сервера)."""
    user = request.user if request.user.is_authenticated else 'Аноним'
    employees_logger.critical("Ошибка 500. Пользователь: %s", user)
    return render(request, '500.html', status=500)


# =====================
# 🔹 По регионам
# =====================
class RegionSelectForm(forms.Form):
    """Форма выбора региона для фильтрации сотрудников."""

    region = forms.ModelChoiceField(
        queryset=Region.objects.all(),
        required=True,
        label='Выберите регион',
    )


@login_required
def employees_by_region(request):
    """Отображает сотрудников выбранного региона."""
    employees = []
    selected_region = None
    form = RegionSelectForm(request.GET or None)

    if form.is_valid():
        selected_region = form.cleaned_data['region']

        # Канонизируем URL: всегда один параметр ?region=<id>
        if selected_region and (
            list(request.GET.keys()) != ['region']
            or request.GET.get('region') != str(selected_region.id)
        ):
            return redirect(
                f"{reverse('employees_by_region')}?region={selected_region.id}"
            )

        if selected_region:
            employees = Employee.objects.filter(region_name=selected_region)

            if not employees.exists():
                messages.warning(
                    request, f'В регионе {selected_region} нет сотрудников.'
                )

    return render(
        request,
        'employees_by_region.html',
        {
            'form': form,
            'employees': employees,
            'selected_region': selected_region,
        },
    )


@login_required
def bulk_delete_employees(request):
    """Массовое удаление сотрудников (только admin)."""
    if not request.user.is_admin:
        messages.error(request, "Удаление доступно только администраторам.")
        return redirect("search_employee")

    if request.method == "POST":
        selected_ids = request.POST.getlist("selected")
        prev_url = request.POST.get("prev_url", reverse("search_employee"))

        if not selected_ids:
            messages.warning(request, "Вы не выбрали сотрудников для удаления.")
            return redirect(prev_url)

        employees = Employee.objects.filter(pk__in=selected_ids)

        if not employees.exists():
            messages.error(request, "Выбранные сотрудники не найдены.")
            return redirect(prev_url)

        # Подтверждение удаления
        if request.POST.get("confirm") == "yes":
            count = employees.count()
            employees.delete()
            messages.success(request, f"Удалено сотрудников: {count}.")
            return redirect(prev_url)

        return render(
            request,
            "bulk_delete_confirm.html",
            {"employees": employees, "prev_url": prev_url},
        )

    return redirect("search_employee")
