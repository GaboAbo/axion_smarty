from django.urls import path, include
from rest_framework.routers import DefaultRouter

from Entity.Views.crud_views import GetAllClients, GetAllContracts

from .views import EntityViewSet, ContractViewSet, AreaViewSet

router = DefaultRouter()
router.register(r"entity", EntityViewSet)
router.register(r"contract", ContractViewSet)
router.register(r"area", AreaViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('getAllClients', GetAllClients, name='getAllClients'),
    path('getAllContracts', GetAllContracts, name='getAllContracts'),
]