from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .Views.crud_views import (
    GetAllOrders,
    GetOrderByID,
    FilterOrder,
    CreateOrder,
    UpdateOrder,
    DeleteOrder,
    DevicesByClient,
    ContractByClient,
    ProtocolsByOrder,
)

from .Views.serializer_views import (
    OrderViewSet,
    MaintenanceViewSet,
)


router = DefaultRouter()
router.register(r"order", OrderViewSet)
router.register(r"protocol", MaintenanceViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('getAllOrders', GetAllOrders, name='getAllOrders'),
    path('filterOrder', FilterOrder, name='filterOrder'),
    path('getOrder/<str:order_id>', GetOrderByID, name='getOrder'),
    path('createOrder', CreateOrder, name='createOrder'),
    path('updateOrder/<str:order_pk>', UpdateOrder, name='updateOrder'),
    path('deleteOrder/<str:order_pk>', DeleteOrder, name='deleteOrder'),
    path('devicesByClient', DevicesByClient, name='devicesByClient'),
    path('contractsByClient', ContractByClient, name='contractsByClient'),
    path('protocolsByOrder/<str:order_pk>', ProtocolsByOrder, name='protocolsByOrder'),
]
