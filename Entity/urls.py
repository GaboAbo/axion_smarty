from django.urls import path, include
from rest_framework.routers import DefaultRouter

from Entity.Views.crud_views import GetAllClients, GetAllContracts
from .views import EntityViewSet, ContractViewSet, AreaViewSet

""" 
Router setup for the Entity app.
Registers viewsets for Entity, Contract, and Area models 
to handle standard CRUD operations through DRF's ModelViewSet.
"""
router = DefaultRouter()
router.register(r"entity", EntityViewSet)
router.register(r"contract", ContractViewSet)
router.register(r"area", AreaViewSet)

"""
Defines URL patterns for the Entity app.

Includes:
- Router-based endpoints for CRUD operations.
- Custom function-based views for fetching all clients and contracts.
"""
urlpatterns = [
    path('', include(router.urls)),

    path('getAllClients', GetAllClients, name='getAllClients'),
    path('getAllContracts', GetAllContracts, name='getAllContracts'),
]
