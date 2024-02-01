from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .chatbot import ChatBot
from .models import Step, Log
from .serializers import ChatSerializer

GREETING = ("hello", "hi", "greetings", "sup", "what’s up", "hey", "yo")
GOODBYE = ("goodbye", "bye", "farewell", "see you", "adios", "see ya")


class ChatView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def is_greeting(text: str):
        for word in text.split():
            if word.lower() in GREETING:
                return True
        return False

    @staticmethod
    def is_ending(text: str):
        for word in text.split():
            if word.lower() in GOODBYE:
                return True
        return False

    def get(self, request):
        data = {'text': 'Welcome to the ChatBot!'}
        serializer = ChatSerializer(data=data)
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ChatSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            user = request.user
            text = data['text']
            response = None

            step, exists = Step.objects.get_or_create(user=user)

            if exists:
                if step.name == 'E':
                    step = Step.objects.create(user=user)

            chat_bot = ChatBot(text)

            if step.name == 'G' or self.is_greeting(text):
                Log(text=text, sender='U', step=step).save()
                step.name = 'Q'
                step.save()
                response = 'Hello, I am Chatty. Ask me some questions.'
                Log(text=response, sender='C', step=step).save()
            elif self.is_ending(text):
                Log(text=text, sender='U', step=step).save()
                step.name = 'E'
                step.save()
                response = 'Bye. Have a nice day!'
                Log(text=response, sender='C', step=step).save()
            elif step.name == 'Q':
                Log(text=text, sender='U', step=step).save()
                response = chat_bot.get_response()
                Log(text=response, sender='C', step=step).save()

            return Response({'text': response}, status=status.HTTP_201_CREATED)
        else:
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
