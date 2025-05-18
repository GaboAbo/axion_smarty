"""
URL routing configuration for the 'Order' domain.

This module defines API routes for working with maintenance orders and protocols,
including viewsets for read/write operations, as well as utility endpoints for
querying devices, contracts, and related protocols.

Routes:
    - 'order/' → DRF ViewSet for Order model (CRUD operations)
    - 'protocol/' → DRF ViewSet for MaintenanceProtocol model
    - 'orders/all/' → List all orders
    - 'orders/filter/' → Filter orders by query parameters
    - 'orders/<order_id>/' → Retrieve an order by ID
    - 'orders/create/' → Create a new order
    - 'orders/<order_pk>/update/' → Update an existing order
    - 'orders/<order_pk>/delete/' → Delete an order
    - 'orders/<order_pk>/protocols/' → Get all protocols linked to an order
    - 'devices/by-client/' → Retrieve all devices linked to a client
    - 'contracts/by-client/' → Retrieve all contracts linked to a client
"""

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

# DRF viewsets for Order and MaintenanceProtocol
router = DefaultRouter()
router.register(r'order', OrderViewSet, basename='order')
router.register(r'protocol', MaintenanceViewSet, basename='protocol')

urlpatterns = [
    # ViewSet-based routes (CRUD)
    path('', include(router.urls)),

    # Order API endpoints
    path('orders/all/', GetAllOrders, name='getAllOrders'),  # List all orders
    path('orders/filter/', FilterOrder, name='filterOrder'),  # Filter orders
    path('orders/<str:order_id>/', GetOrderByID, name='getOrder'),  # Retrieve by ID
    path('orders/create/', CreateOrder, name='createOrder'),  # Create order
    path('orders/<str:order_pk>/update/', UpdateOrder, name='updateOrder'),  # Update
    path('orders/<str:order_pk>/delete/', DeleteOrder, name='deleteOrder'),  # Delete
    path('orders/<str:order_pk>/protocols/', ProtocolsByOrder, name='protocolsByOrder'),  # Related protocols

    # Related resource endpoints
    path('devices/by-client/', DevicesByClient, name='devicesByClient'),  # Devices linked to a client
    path('contracts/by-client/', ContractByClient, name='contractsByClient'),  # Contracts linked to a client
]
