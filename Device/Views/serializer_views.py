from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet


from ..models import (
    DeviceModel,
    Device,
)


from ..serializers import (
    DeviceModelSerializer,
    DeviceSerializer,
)


# Create your views here.
class DeviceModelViewSet(viewsets.ModelViewSet):
    queryset = DeviceModel.objects.all()
    serializer_class = DeviceModelSerializer


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.select_related("client", "device_model")
    serializer_class = DeviceSerializer

