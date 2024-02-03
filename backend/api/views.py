from django.contrib.auth.models import User
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .chatbot import ChatBot
from .models import Step, Log
from .serializers import ChatSerializer, RegisterSerializer

GREETING = ("hello", "hi", "greetings", "sup", "what’s up", "hey", "yo")
GOODBYE = ("goodbye", "bye", "farewell", "see you", "adios", "see ya")


class HomeView(APIView):
    """
    API view for API home page
    """
    permission_classes = (AllowAny,)

    def get(self, request):
        """
        Handle GET requests by returning a welcome message.

        Parameters:
        - request (Request): The HTTP request object.

        Returns:
        - Response: A Response object containing a welcome message and a status of 200 OK.
        """
        data = {'text': 'Welcome to the ChatBot!'}
        return Response(data, status=status.HTTP_200_OK)


class ChatView(APIView):
    """
    API view for handling chat interactions with a ChatBot.

    This view supports POST requests. Authentication is required, and
    the `IsAuthenticated` permission class is applied.

    HTTP Methods:
    - POST: Handles user input, processes it with a ChatBot, and returns the generated response.

    Permissions:
    - Requires authentication using the `IsAuthenticated` permission class.

    Attributes:
    - GREETING (tuple): A tuple containing phrases considered as greetings.
    - GOODBYE (tuple): A tuple containing phrases considered as goodbyes.

    Methods:
    - is_greeting(text: str) -> bool: Check if the input text contains a greeting.
    - is_ending(text: str) -> bool: Check if the input text contains a goodbye.
    - save_step(step: Step, name: str, text: str): Save the current step and log a user's input.

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

    @staticmethod
    def is_greeting(text: str) -> bool:
        """
        Check if the input text contains a greeting.

        Parameters:
        - text (str): The input text to be checked.

        Returns:
        - bool: True if a greeting is found; otherwise, False.
        """
        for word in text.split():
            if word.lower() in GREETING:
                return True
        return False

    @staticmethod
    def is_ending(text: str) -> bool:
        """
        Check if the input text contains a goodbye.

        Parameters:
        - text (str): The input text to be checked.

        Returns:
        - bool: True if a goodbye is found; otherwise, False.
        """
        for word in text.split():
            if word.lower() in GOODBYE:
                return True
        return False

    @staticmethod
    def save_step(step: Step, name: str, text: str):
        """
        Save the current step and log a user's input.

        Parameters:
        - step (Step): The Step instance associated with the user.
        - name (str): The name of the step to be saved.
        - text (str): The user's input text.
        """
        step.name = name
        step.save()
        Log(step=step, sender='U', text=text).save()

    def post(self, request):
        """
        Handle POST requests by processing user input and returning the ChatBot's response.

        Parameters:
        - request (Request): The HTTP request object.

        Returns:
        - Response: A Response object containing the generated response or errors with appropriate status codes.
        """
        serializer = ChatSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            user = request.user
            text = data['text']
            response = None

            step, exists = Step.objects.get_or_create(user=user)  # get or create new session for a user

            if exists and step.name == 'E':
                step = Step.objects.create(user=user)  # create new session if the previous one has ended

            chat_bot = ChatBot.from_json(data)

            if step.name == 'G' or self.is_greeting(text):
                self.save_step(step, 'Q', text)
                response = 'Hello, I am Chatty. Ask me some questions.'
                Log(text=response, sender='C', step=step).save()
            elif self.is_ending(text):
                self.save_step(step, 'E', text)
                response = 'Bye. Have a nice day!'
                Log(text=response, sender='C', step=step).save()
            elif step.name == 'Q':
                self.save_step(step, 'Q', text)
                response = chat_bot.get_response()
                Log(text=response, sender='C', step=step).save()

            return Response({'text': response}, status=status.HTTP_201_CREATED)
        else:
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
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

    def post(self, request):
        """
        Handle user logout by blacklisting refresh tokens.

        Parameters:
        - request (Request): The HTTP request object.

        Returns:
        - Response: A Response object with a status of 205 Reset Content upon success.
                    A Response object with a status of 400 Bad Request if there is an exception during the process.
        """
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
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
