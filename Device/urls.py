from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .Views.serializer_views import DeviceModelViewSet
from .Views.crud_views import GetAllDevices, FilterDevice

router = DefaultRouter()
router.register(r"model-device", DeviceModelViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('get-all-devices/', GetAllDevices, name='getAllDevices'),
    path('filter-device/', FilterDevice, name='filter_device'),
]
