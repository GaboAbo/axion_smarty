"""
Views for the AuthUser app.

Defines a viewset for managing Engineer instances via the Django REST framework.
"""

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Engineer
from .serializers import EngineerSerializer


class EngineerViewSet(ModelViewSet):
    """
    ViewSet for handling Engineer model operations.

    This ViewSet provides `list`, `create`, `retrieve`, `update`, and `destroy` actions
    for the Engineer model. It uses a partial update by default to simplify PATCH support.
    """
    queryset = Engineer.objects.all()
    serializer_class = EngineerSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        """
        Override the default update behavior to allow partial updates by default.

        This means clients don't need to specify all required fields in a PUT request.
        """
        partial = True
        return super().update(request, partial=partial, *args, **kwargs)
