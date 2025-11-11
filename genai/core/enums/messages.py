from enum import Enum


class OpenAIChat(Enum):
    ASSISTANT = "assistant"
    USER = "user"

    ROLE = "role"
    CONTENT = "content"


class GeminiChat(Enum):
    ASSISTANT = "model"
    USER = "user"

    ROLE = "role"
    CONTENT = "parts"
