from rest_framework import serializers


class ParentSerializer(serializers.ModelSerializer):
    """
    __init__ (overriden): Dinamically set the desired fields

    Gets the fields specified in the context, which is passed by the child serializer

    If there are fields passed, converts such fields into a set and store it in allowed
    Then, converts the Meta fields into a set and store it in existing

    Arithmetic operations are allowed between sets, so allowed fields are subtracted from the existing fields
    Finally, it iterates through the result from the previous operation and pops the remained fields from the Meta(not allowed)

    __init__ executes every time the constructor is called
    As a result, if there are passed fields, the serializer will only include them
    If there are not fields passed, it will not set any fields from the parent serializer
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields = self.context.get('fields', None)
        if fields:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
