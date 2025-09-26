from django.urls import path, include

from . import views

"""URL-конфигурация приложения employees."""

urlpatterns = [
    # 🔹 Главная и справка
    path('', views.index, name='index'),
    path('help/', views.help, name='help'),

    # 🔹 Авторизация
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # 🔹 CRUD сотрудников
    path('create/', views.create_employee, name='create_employee'),
    path('search/', views.search_employee, name='search_employee'),
    path('edit/<int:pk>/', views.edit_employee, name='edit_employee'),
    path('delete/<int:pk>/', views.delete_employee, name='delete_employee'),

    # 🔹 Вспомогательные функции
    path('export_confirm/', views.confirm_export, name='confirm_export'),
    path('export_excel/', views.export_excel, name='export_excel'),
    path(
        'generate_password/',
        views.generate_password_view,
        name='generate_password',
    ),
    path(
        'employees_by_region/',
        views.employees_by_region,
        name='employees_by_region',
    ),
    path("bulk_delete/", views.bulk_delete_employees, name="bulk_delete_employees"),
]

# Кастомные обработчики ошибок
handler403 = 'employees.views.error_403'
handler404 = 'employees.views.error_404'
handler500 = 'employees.views.error_500'
