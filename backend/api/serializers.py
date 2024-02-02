from rest_framework import serializers

from backend.api.models import Step, Log


class ChatSerializer(serializers.Serializer):
    """
    Serializer for handling chat-related data.

    Attributes:
    - text (str): The text content of the chat message.
    """
    text = serializers.CharField()


class StepSerializer(serializers.Serializer):
    """
    Serializer for the Step model.

    This serializer is used to convert Step model instances to JSON and vice versa.

    Attributes:
    - model (Step): The Step model class associated with this serializer.
    - fields (list): A list of field names to include in the serialized representation.

    """

    class Meta:
        model = Step
        fields = '__all__'


class LogSerializer(serializers.Serializer):
    """
    Serializer for the Log model.

    This serializer is used to convert Log model instances to JSON and vice versa.

    Attributes:
    - model (Log): The Log model class associated with this serializer.
    - fields (list): A list of field names to include in the serialized representation.

    """

    class Meta:
        model = Log
        fields = '__all__'
