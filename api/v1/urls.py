from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

from .views import EmployeeViewSet, RegionViewSet

# Роутер для CRUD API
router = DefaultRouter()
router.register(r'employees', EmployeeViewSet, basename='employee')
router.register(r'regions', RegionViewSet, basename='region')

urlpatterns = [
    # JWT авторизация
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # OpenAPI схема
    path('schema/', SpectacularAPIView.as_view(), name='schema'),

    # Swagger UI
    path(
        'docs/swagger/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui',
    ),

    # ReDoc
    path(
        'docs/redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc',
    ),
]

# Подключаем CRUD-маршруты из роутера
urlpatterns += router.urls
