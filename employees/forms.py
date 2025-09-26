import re

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Employee, Region


def validate_russian_name(value):
    """
    Валидатор для ФИО:
    разрешает только русские буквы, первая буква — заглавная.
    """
    if not re.match(r"^[А-ЯЁ][а-яё]+$", value):
        raise ValidationError(
            "Разрешены только русские буквы. "
            "Первая буква должна быть заглавной."
        )


# ========== Форма создания/редактирования сотрудника ==========
class EmployeeForm(forms.ModelForm):
    """Форма для создания и редактирования сотрудника."""

    last_name = forms.CharField(
        label="Фамилия",
        validators=[validate_russian_name],
        widget=forms.TextInput(
            attrs={
                "placeholder": "Фамилия",
                "class": "w-full border rounded-md px-3 py-2 shadow-sm "
                         "focus:ring focus:ring-indigo-200 focus:border-indigo-500",
            }
        ),
    )
    first_name = forms.CharField(
        label="Имя",
        validators=[validate_russian_name],
        widget=forms.TextInput(
            attrs={
                "placeholder": "Имя",
                "class": "w-full border rounded-md px-3 py-2 shadow-sm "
                         "focus:ring focus:ring-indigo-200 focus:border-indigo-500",
            }
        ),
    )
    patronymic = forms.CharField(
        label="Отчество",
        required=False,
        validators=[validate_russian_name],
        widget=forms.TextInput(
            attrs={
                "placeholder": "Отчество",
                "class": "w-full border rounded-md px-3 py-2 shadow-sm "
                         "focus:ring focus:ring-indigo-200 focus:border-indigo-500",
            }
        ),
    )
    note_date = forms.DateField(
        label="Дата служебной записки",
        widget=forms.DateInput(
            format="%Y-%m-%d",
            attrs={
                "type": "date",
                "class": "w-full border rounded-md px-3 py-2 shadow-sm "
                         "focus:ring focus:ring-indigo-200 focus:border-indigo-500",
            },
        ),
        input_formats=["%Y-%m-%d"],
        required=False,
    )
    note_number = forms.CharField(
        label="Номер служебной записки",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Номер служебной записки",
                "class": "w-full border rounded-md px-3 py-2 shadow-sm "
                         "focus:ring focus:ring-indigo-200 focus:border-indigo-500",
            }
        ),
    )

    class Meta:
        model = Employee
        fields = [
            "last_name",
            "first_name",
            "patronymic",
            "region_name",
            "note_date",
            "note_number",
            "status",
        ]
        widgets = {
            "region_name": forms.Select(
                attrs={
                    "class": "w-full border rounded-md px-3 py-2 h-10 shadow-sm "
                             "focus:ring focus:ring-indigo-200 focus:border-indigo-500",
                }
            ),
            "status": forms.Select(
                attrs={
                    "class": "w-full border rounded-md px-3 py-2 h-10 shadow-sm "
                             "focus:ring focus:ring-indigo-200 focus:border-indigo-500",
                }
            ),
        }

    def clean_note_date(self):
        """Не допускаем будущую дату."""
        date = self.cleaned_data.get("note_date")
        if date and date > timezone.localdate():
            raise ValidationError("Дата не может быть из будущего.")
        return date


# ========== Форма поиска сотрудников ==========
class SearchForm(forms.Form):
    """Форма для поиска сотрудников."""

    last_name = forms.CharField(
        required=False,
        label="Фамилия",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Фамилия",
                "class": "w-full border rounded-md px-3 py-2 shadow-sm "
                         "focus:ring focus:ring-indigo-200 focus:border-indigo-500",
            }
        ),
    )
    first_name = forms.CharField(
        required=False,
        label="Имя",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Имя",
                "class": "w-full border rounded-md px-3 py-2 shadow-sm "
                         "focus:ring focus:ring-indigo-200 focus:border-indigo-500",
            }
        ),
    )
    patronymic = forms.CharField(
        required=False,
        label="Отчество",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Отчество",
                "class": "w-full border rounded-md px-3 py-2 shadow-sm "
                         "focus:ring focus:ring-indigo-200 focus:border-indigo-500",
            }
        ),
    )
    region_name = forms.ModelChoiceField(
        queryset=Region.objects.all(),
        required=False,
        label="Регион",
        widget=forms.Select(
            attrs={
                "class": "w-full border rounded-md px-3 py-2 h-10 shadow-sm "
                         "focus:ring focus:ring-indigo-200 focus:border-indigo-500",
            }
        ),
    )
    note_date = forms.DateField(
        required=False,
        label="Дата служебной записки",
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "w-full border rounded-md px-3 py-2 shadow-sm "
                         "focus:ring focus:ring-indigo-200 focus:border-indigo-500",
            }
        ),
    )
    note_number = forms.CharField(
        required=False,
        label="Номер служебной записки",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Номер служебной записки",
                "class": "w-full border rounded-md px-3 py-2 shadow-sm "
                         "focus:ring focus:ring-indigo-200 focus:border-indigo-500",
            }
        ),
    )
    status = forms.ChoiceField(
        required=False,
        label="Статус",
        choices=[("", "---")] + Employee.STATUSES,
        widget=forms.Select(
            attrs={
                "class": "w-full border rounded-md px-3 py-2 h-10 shadow-sm "
                         "focus:ring focus:ring-indigo-200 focus:border-indigo-500",
            }
        ),
    )
    created_at = forms.DateField(
        required=False,
        label="Дата создания",
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "w-full border rounded-md px-3 py-2 shadow-sm "
                         "focus:ring focus:ring-indigo-200 focus:border-indigo-500",
            }
        ),
    )

    def clean_note_date(self):
        """Не допускаем будущую дату при поиске."""
        date = self.cleaned_data.get("note_date")
        if date and date > timezone.localdate():
            raise ValidationError("Дата не может быть из будущего.")
        return date

    def clean_created_at(self):
        """Не допускаем будущую дату создания."""
        date = self.cleaned_data.get("created_at")
        if date and date > timezone.localdate():
            raise ValidationError("Дата не может быть из будущего.")
        return date


class RegionSelectForm(forms.Form):
    """Форма выбора региона для фильтра сотрудников."""

    region = forms.ModelChoiceField(
        queryset=Region.objects.all(),
        required=False,
        label="Регион",
        widget=forms.Select(
            attrs={
                "class": (
                    "w-full border rounded-md px-3 py-2 h-10 shadow-sm "
                    "focus:ring focus:ring-indigo-200 "
                    "focus:border-indigo-500"
                ),
            }
        ),
    )
