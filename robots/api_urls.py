"""API URLs do app Robots (Django REST Framework)"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import RobotViewSet

router = DefaultRouter()
router.register(r'robots', RobotViewSet, basename='robot')

urlpatterns = [
    path('', include(router.urls)),
]
