from ..interfaces.chatbot_interface import ChatBotInterface
from ..interfaces.log_interface import LogInterface
from ..interfaces.step_interface import StepInterface

GREETING = ("hello", "hi", "greetings", "sup", "what’s up", "hey", "yo")
GOODBYE = ("goodbye", "bye", "farewell", "see you", "adios", "see ya")


class ChatBotService(object):
    def __init__(self, chatbot: ChatBotInterface, log_repository: LogInterface,
                 step_repository: StepInterface):
        self._chatbot = chatbot
        self._log_repository = log_repository
        self._step_repository = step_repository
        self._response = None
        self._state = None
        self._text = None
        self._step = None

    def get_response(self):
        self._step = self._step_repository.get()  # get session for a user

        if not self._step or self._step.name == 'E':
            self._step = self._step_repository.create()  # create new session if the previous one has ended

        self._text = self._chatbot.get_text()

        if self._step.name == 'G' or self.is_greeting():
            self._state = 'Q'
            self._response = 'Hello, I am Chatty. Ask me some questions.'
        elif self.is_ending():
            self._state = 'E'
            self._response = 'Bye. Have a nice day!'
        elif self._step.name == 'Q':
            self._state = 'Q'
            self._response = self._chatbot.get_response()

        self._save_step()
        return self._response

    def _save_step(self):
        self._log_repository.create(self._text, 'U', self._step)
        self._step_repository.update(self._state, self._step)
        self._log_repository.create(self._response, 'C', self._step)

    def is_greeting(self):
        """
        Check if the input text contains a greeting.
        """
        for word in self._text.split():
            if word.lower() in GREETING:
                return True
        return False

    def is_ending(self):
        """
        Check if the input text contains a goodbye.
        """
        for word in self._text.split():
            if word.lower() in GOODBYE:
                return True
        return False
