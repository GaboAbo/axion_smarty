from rest_framework import viewsets

from .models import Entity, Contract, Area
from .serializers import EntitySerializer, ContractSerializer, AreaSerializer

"""
ViewSets for the Entity app.

Each viewset handles the standard CRUD operations 
for the Entity, Contract, and Area models.
"""


class EntityViewSet(viewsets.ModelViewSet):
    """
    Provides CRUD operations for Entity instances.
    """
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer


class ContractViewSet(viewsets.ModelViewSet):
    """
    Provides CRUD operations for Contract instances.
    Uses select_related to optimize queries involving the related Entity.
    """
    queryset = Contract.objects.select_related("entity")
    serializer_class = ContractSerializer


class AreaViewSet(viewsets.ModelViewSet):
    """
    Provides CRUD operations for Area instances.
    """
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
