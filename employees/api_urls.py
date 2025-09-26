from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views_api import EmployeeViewSet, RegionViewSet

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet, basename='employee')
router.register(r'regions', RegionViewSet, basename='region')

urlpatterns = [
    path('', include(router.urls)),
]
