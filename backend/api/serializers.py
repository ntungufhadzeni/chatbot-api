from rest_framework import serializers


class ChatSerializer(serializers.Serializer):
    """
    Serializer for handling chat-related data.

    Attributes:
    - text (str): The text content of the chat message.
    """
    text = serializers.CharField()
