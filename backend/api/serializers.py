from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class ChatSerializer(serializers.Serializer):
    """
    Serializer for handling chat-related data.

    Attributes:
    - text (str): The text content of the chat message.
    """
    text = serializers.CharField()


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    This serializer validates and processes the data for creating a new user account.

    Fields:
    - username (str): The desired username for the new user account.
    - email (str): The email address for the new user account.
    - password (str): The password for the new user account.
    - password2 (str): Confirmation of the password for validation.

    Validations:
    - The password and password2 fields must match for successful validation.

    Methods:
    - validate(attrs): Custom validation method to ensure password and password2 match.
    - create(validated_data): Custom method to create a new user account.

    Example Usage:
    ```python
    # Example usage of RegisterSerializer in a view
    serializer = RegisterSerializer(data={'username': 'newuser', 'email': 'newuser@example.com', 'password': 'password', 'password2': 'password'})
    if serializer.is_valid():
        user_instance = serializer.save()
    ```

    Note:
    - Make sure to provide the necessary fields for successful user registration.
    - Password and password2 must match for successful registration.
    """
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, attrs):
        """
        Custom validation method to ensure password and password2 fields match.

        Parameters:
        - attrs (dict): The dictionary containing the serializer data.

        Raises:
        - serializers.ValidationError: If password and password2 fields do not match.

        Returns:
        - dict: The validated data.
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        """
        Custom method to create a new user account.

        Parameters:
        - validated_data (dict): The validated data for creating a new user account.

        Returns:
        - User: The newly created user instance.
        """
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
