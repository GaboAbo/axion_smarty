from rest_framework import serializers

from .models import Entity, Contract, Area


class EntitySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Entity
        fields = [
            "id",
            "name",
            "address",
        ]


class ContractSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source="entity.name", read_only=True)

    class Meta:
        model = Contract
        fields = [
            "id",
            "number",
            "client_name",
            "contract_type",
            "start_date",
            "end_date",
        ]


class AreaSerializer(serializers.ModelSerializer):
    entity = EntitySerializer(read_only=True)

    class Meta:
        model = Area
        fields = "__all__"
