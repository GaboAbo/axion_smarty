from .models import Engineer

from rest_framework import serializers


class EngineerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Engineer
        fields = ["id", "first_name", "last_name", "email", "role", "signature"]