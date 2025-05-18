from rest_framework import serializers

from .models import Entity, Contract, Area


class EntitySerializer(serializers.ModelSerializer):
    """
    Serializer for the Entity model.

    Provides basic fields such as name and address of a hospital, clinic, or institute.
    """

    class Meta:
        model = Entity
        fields = [
            "id",
            "name",
            "address",
        ]


class ContractSerializer(serializers.ModelSerializer):
    """
    Serializer for the Contract model.

    Includes basic contract fields along with the related entity's name as `client_name`.
    """

    client_name = serializers.CharField(
        source="entity.name",
        read_only=True,
        help_text="Name of the entity associated with the contract."
    )

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
    """
    Serializer for the Area model.

    Embeds the full `EntitySerializer` for read-only display of related entity information.
    """

    entity = EntitySerializer(read_only=True)

    class Meta:
        model = Area
        fields = "__all__"
