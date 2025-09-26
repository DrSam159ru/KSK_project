from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import EmployeeViewSet, RegionViewSet, PasswordPolicyViewSet

app_name = "api_v1"

router = DefaultRouter()
router.register(r"employees", EmployeeViewSet, basename="employee")
router.register(r"regions", RegionViewSet, basename="region")
router.register(r"password-policies", PasswordPolicyViewSet, basename="passwordpolicy")

urlpatterns = [
    path("", include(router.urls)),
]
