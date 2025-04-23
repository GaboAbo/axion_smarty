from rest_framework import viewsets

from .models import Entity, Contract, Area
from .serializers import EntitySerializer, ContractSerializer, AreaSerializer


# Create your views here.
class EntityViewSet(viewsets.ModelViewSet):
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer


class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.select_related("entity")
    serializer_class = ContractSerializer


class AreaViewSet(viewsets.ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
