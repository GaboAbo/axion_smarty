import base64

from django.core.files.base import ContentFile

from rest_framework import serializers

from .models import Order, MaintenanceProtocol

from App.serializers import ParentSerializer


class MaintenanceListSerializer(ParentSerializer):
    device_type = serializers.CharField(source="device.device_model.device_type.name", read_only=True)
    device_model = serializers.CharField(source="device.device_model.part_number", read_only=True)
    device_serial = serializers.CharField(source="device.serial_number", read_only=True)
    device_contract = serializers.CharField(source="device.contract", read_only=True)

    class Meta:
        model = MaintenanceProtocol
        fields = [
            "id",
            "order",
            "device_type",
            "device_model",
            "device_serial",
            "device_contract",
            "location",
            "status",
        ]


class MaintenanceSerializer(ParentSerializer):
    device_type = serializers.CharField(source="device.device_model.device_type.name", read_only=True)
    device_model = serializers.CharField(source="device.device_model.part_number", read_only=True)
    device_serial = serializers.CharField(source="device.serial_number", read_only=True)
    device_contract = serializers.CharField(source="device.contract", read_only=True)

    class Meta:
        model = MaintenanceProtocol
        fields = [
            "id",
            "order",
            "device_type",
            "device_model",
            "device_serial",
            "device_contract",
            "location",
            "status",
            "fields",
        ]


class OrderListSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source="client.name", read_only=True)
    client_address = serializers.CharField(source="client.address", read_only=True)
    created_at = serializers.DateField(format='%b. %d, %Y', read_only=True)

    class Meta:
        model = Order
        fields = [
           "id",
           "client_name",
           "client_address",
           "created_at",
           "status",
           "client_sign",
           "client_personal_name",
        ]


class OrderSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source="client.name", read_only=True)
    client_address = serializers.CharField(source="client.address", read_only=True)
    created_at = serializers.DateField(format='%b. %d, %Y', read_only=True)

    maintenance_protocols = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = [
           "id",
           "client_name",
           "client_address",
           "created_at",
           "status",
           "maintenance_protocols",
           "client_sign",
           "client_personal_name",
        ]
        
    def get_maintenance_protocols(self, obj):
        protocols = []
        fields = ["id", "device_model", "device_serial", "status"]
        mts = MaintenanceProtocol.objects.filter(order=obj)
        protocols.extend(MaintenanceSerializer(mts, context={'fields': fields}, many=True).data)
        return protocols
