from rest_framework import serializers

from .models import DeviceModel, Device

from Entity.models import Entity
from Entity.serializers import EntitySerializer, ContractSerializer, AreaSerializer

from App.serializers import ParentSerializer


class DeviceModelSerializer(ParentSerializer):
    
    class Meta:
        model = DeviceModel
        fields = [
            "id",
            "part_number"
        ]


class DeviceSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source="client.name", read_only=True)
    device_model = serializers.CharField(source="device_model.part_number", read_only=True)

    class Meta:
        model = Device
        fields = [
            "id",
            "client_name",
            "device_model",
            "serial_number",
        ]
