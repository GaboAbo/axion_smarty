"""
URL routing for the AuthUser app.

Defines the API endpoints related to the Engineer model, registering the
EngineerViewSet with the DefaultRouter and including the generated URLs.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import EngineerViewSet

# Initialize the DefaultRouter and register the EngineerViewSet.
router = DefaultRouter()
router.register(r"engineer", EngineerViewSet)

urlpatterns = [
    # Include the generated URLs from the router for the 'engineer' viewset.
    path('', include(router.urls)),
]
