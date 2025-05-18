from rest_framework import serializers

from .models import DeviceModel, Device
from Entity.models import Entity, Contract
from Entity.serializers import EntitySerializer, ContractSerializer

from App.serializers import ParentSerializer


class DeviceModelSerializer(ParentSerializer):
    """
    Serializer for the DeviceModel model.
    Only includes minimal fields (ID and part number).
    """
    class Meta:
        model = DeviceModel
        fields = [
            "id",
            "part_number",
        ]


class DeviceSerializer(serializers.ModelSerializer):
    """
    Read-only serializer for Device model.
    Includes human-readable client and device model names.
    """
    client_name = serializers.CharField(source="client.name", read_only=True)
    device_model_name = serializers.CharField(source="device_model.part_number", read_only=True)

    class Meta:
        model = Device
        fields = [
            "id",
            "client_name",
            "device_model_name",
            "serial_number",
        ]
