from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated


from ..models import (
    Order,
    MaintenanceProtocol,
)


from ..serializers import (
    OrderSerializer,
    OrderListSerializer,
    MaintenanceListSerializer,
    MaintenanceSerializer
)


# Create your views here.
class OrderViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    queryset = Order.objects.select_related("client")
    serializer_class = OrderSerializer
    
    def get_serializer_class(self):
        if self.action == 'list':
            return OrderListSerializer
        if self.action == 'retrieve':
            return OrderSerializer
        return super().get_serializer_class()


class MaintenanceViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    queryset = MaintenanceProtocol.objects.select_related("device")
    serializer_class = MaintenanceSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return MaintenanceListSerializer
        if self.action == 'retrieve':
            return MaintenanceSerializer
        return super().get_serializer_class()


