from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import EngineerViewSet


router = DefaultRouter()
router.register(r"engineer", EngineerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]