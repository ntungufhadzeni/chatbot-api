from nltk.chat.util import Chat, reflections

pairs = [
    [
        r"my name is (.*)",
        ["Hello %1, nice to have you here. How can I help you?", ]
    ],
    [
        r"what is your name?",
        ["My name is Chatty.", ]
    ],
    [
        r"how are you ?",
        ["Pretty good, thank you! How are you doing?", ]
    ],
    [
        r"I am fine, thank you",
        ["Great to hear that. How can I help you?", ]
    ],
    [
        r"i'm (.*) doing good",
        ["That's great to hear! How can I assist you?", ]
    ],
    [
        r"(.*) created you?",
        ["Ntungufhadzeni created me.", ]
    ],
    [
        r"how is the weather in (.*)",
        ["The weather in %1 is pretty awesome as always.", ]
    ],
    [
        r"can you help(.*)",
        ["Of course, I can help you.", ]
    ],
    [
        r"(.*)(location|city)(.*)",
        ["I am located in Johannesburg, South Africa.", ]
    ],
    [
        r"(which|what) (.*) (sport|game) ?",
        ["I love soccer.", ]
    ],
    [
        r"thank you so much, that was amazing",
        ["I am happy to help. No problem, you're welcome.", ]
    ],
    [
        r"what is the meaning of life?",
        ["The meaning of life is a philosophical question that has different answers for different people.", ]
    ],
    [
        r"tell me a joke",
        ["Why don't scientists trust atoms? Because they make up everything!", ]
    ],
    [
        r"do you like music?",
        ["I don't have personal preferences, but I can recommend some music if you'd like.", ]
    ],
]


class ChatBot(object):
    def __init__(self, text):
        self._text = text
        self._response = None
        self._chat = Chat(pairs, reflections)

    def get_response(self):
        if not self._response:
            self._set_response()
        return self._response

    def _set_response(self):
        self._response = self._chat.respond(self._text)
        if not self._response:
            self._response = 'Sorry, I did not understand the input. Please try again.'

    @classmethod
    def from_json(cls, json_data):
        return cls(json_data['text'])