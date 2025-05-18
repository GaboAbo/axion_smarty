"""
Serializers for the AuthUser app.

Includes serializers for the Engineer model.
"""

from .models import Engineer
from rest_framework import serializers


class EngineerSerializer(serializers.ModelSerializer):
    """
    Serializer for the Engineer model.

    This serializer converts Engineer model instances into JSON format and vice versa.
    
    Fields:
        id (int): The unique identifier for the engineer.
        first_name (str): The first name of the engineer.
        last_name (str): The last name of the engineer.
        email (str): The email address of the engineer.
        role (str): The role of the engineer within the entity.
        signature (str): The engineer’s signature (used in reports).
    """

    class Meta:
        model = Engineer
        fields = ["id", "first_name", "last_name", "email", "role", "signature"]
