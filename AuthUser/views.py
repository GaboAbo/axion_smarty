from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Engineer

from .serializers import EngineerSerializer


class EngineerViewSet(ModelViewSet):
    queryset = Engineer.objects.all()
    serializer_class = EngineerSerializer

    def update(self, request, *args, **kwargs):
        partial = True
        return super().update(request, partial=partial, *args, **kwargs)