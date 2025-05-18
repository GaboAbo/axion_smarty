"""
Custom serializer base class for selective field serialization.

This module defines a base serializer that allows dynamically including only
specified fields via the serializer's context.
"""

from rest_framework import serializers


class ParentSerializer(serializers.ModelSerializer):
    """
    A base serializer that allows dynamic inclusion of fields.

    This class enables child serializers to specify which fields to include
    by passing a `fields` list in the serializer context.

    Behavior:
        - If `fields` are passed in the context, only those fields will be retained.
        - If no `fields` are passed, all fields defined in the Meta class will be included.

    Example:
        ```python
        serializer = MyChildSerializer(instance, context={'fields': ['id', 'name']})
        ```

    This approach is useful when building flexible APIs or reusable serializers.
    """

    def __init__(self, *args, **kwargs):
        """
        Override the default constructor to dynamically filter fields.

        Args:
            *args: Positional arguments passed to the parent constructor.
            **kwargs: Keyword arguments passed to the parent constructor.

        Notes:
            - This method is called every time the serializer is instantiated.
            - Fields specified in `context['fields']` will be the only ones included.
        """
        super().__init__(*args, **kwargs)
        fields = self.context.get('fields', None)
        if fields:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
