from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # API v1
    path('api/v1/', include('api.v1.urls')),

    # JWT авторизация
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # Перезагрузка для dev
    path("__reload__/", include("django_browser_reload.urls")),

    # HTML-шаблоны (frontend)
    path('', include('employees.urls')),
]

# Кастомные обработчики ошибок
handler403 = 'employees.views.error_403'
handler404 = 'employees.views.error_404'
handler500 = 'employees.views.error_500'
