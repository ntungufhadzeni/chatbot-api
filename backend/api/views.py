from django.contrib.auth.models import User
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .nltk_chatbot import NltkChatBot
from .repositories.log__repository import LogRepository
from .repositories.step_repository import StepRepository
from .serializers import ChatSerializer, RegisterSerializer, LogoutSerializer
from .services.chatbot_service import ChatBotService

GREETING = ("hello", "hi", "greetings", "sup", "what’s up", "hey", "yo")
GOODBYE = ("goodbye", "bye", "farewell", "see you", "adios", "see ya")


class HomeView(APIView):
    """
    API view for the home page.

    Handles GET requests by returning a welcome message.

    Parameters:
    - request (Request): The HTTP request object.

    Returns:
    - Response: A Response object containing a welcome message and a status of 200 OK.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        data = {'text': 'Welcome to the ChatBot API.'}
        return Response(data, status=status.HTTP_200_OK)


class ChatView(generics.GenericAPIView):
    """
    API view for handling chat interactions with a ChatBot.

    This view supports POST requests. Authentication is required, and
    the `IsAuthenticated` permission class is applied.

    HTTP Methods:
    - POST: Handles user input, processes it with a ChatBot, and returns the generated response.

    Permissions:
    - Requires authentication using the `IsAuthenticated` permission class.

    Example Usage:
    ```python
    # Example POST request with user input
    # curl -X POST -H "Authorization: Bearer <your_access_token>" -d '{"text": "Hello, how are you?"}' http://your-api-domain/chat/
    ```

    Note:
    - Ensure that the `IsAuthenticated` permission is applied to restrict access to authenticated users only.
    - Make sure to include the appropriate authentication headers when making requests to this endpoint.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = ChatSerializer

    def post(self, request):
        """
        Handle POST requests by processing user input and returning the ChatBot's response.

        Parameters:
        - request (Request): The HTTP request object.

        Returns:
        - Response: A Response object containing the generated response or errors with appropriate status codes.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            user = request.user

            step_repository = StepRepository(user)
            log_repository = LogRepository()
            chat_bot = NltkChatBot.from_json(data)

            chatbot_service = ChatBotService(chat_bot, log_repository, step_repository)
            response = chatbot_service.get_response()
            data = {'text': response}

            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(generics.GenericAPIView):
    """
    API view for handling user logout by blacklisting refresh tokens.

    This view expects a POST request with a valid refresh token in the request data.
    Upon receiving a valid refresh token, it is blacklisted, effectively logging the user out.

    Permissions:
    - Requires authentication using the `IsAuthenticated` permission class.

    HTTP Methods:
    - POST: Blacklists the provided refresh token, logging the user out.
      Returns a 205 Reset Content status upon success.
      Returns a 400 Bad Request status if there is an exception during the process.

    Example Usage:
    ```python
    # Example POST request with a valid refresh token
    # curl -X POST -H "Authorization: Bearer <your_refresh_token>" http://your-api-domain/logout/
    ```

    Note:
    - Ensure that the `IsAuthenticated` permission is applied to restrict access to authenticated users only.
    - Make sure to include the appropriate authentication headers when making requests to this endpoint.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = LogoutSerializer

    def post(self, request):
        """
        Handle user logout by blacklisting refresh tokens.

        Parameters:
        - request (Request): The HTTP request object.

        Returns:
        - Response: A Response object with a status of 205 Reset Content upon success.
                    A Response object with a status of 400 Bad Request if there is an exception during the process.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            refresh_token = serializer.validated_data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class RegisterView(generics.CreateAPIView):
    """
    API view for user registration.

    This view allows users to register by providing their username, email, and password.
    Upon successful registration, a new user account is created.

    HTTP Methods:
    - POST: Create a new user account by providing the required registration information.

    Request Parameters (POST):
    - username (str): The desired username for the new user account.
    - email (str): The email address for the new user account.
    - password (str): The password for the new user account.
    - password2 (str): Confirmation of the password for validation.

    Returns:
    - Response: A Response object indicating the result of the registration process.

    Example Usage:
    ```python
    # Example POST request to register a new user
    # curl -X POST http://your-api-domain/register/ -d "username=newuser&email=newuser@example.com&password=password&password2=password"
    ```

    Note:
    - Make sure to provide the necessary parameters in the request body for successful registration.
    - Password and password2 must match for successful registration.
    """
    queryset = User.objects.all()
    permission_classes = [AllowAny, ]
    serializer_class = RegisterSerializer
