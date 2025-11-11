from abc import ABC, abstractmethod
from pydantic import BaseModel


class BaseNLP(ABC):
    @abstractmethod
    def connect(self): ...

    @abstractmethod
    def disconnect(self): ...

    @abstractmethod
    def create_user_message(self, user_message: str) -> dict: ...

    @abstractmethod
    def create_model_message(self, model_message: str) -> dict: ...

    @abstractmethod
    def embed(
        self, queries: list[str], batch_size: int, model_name: str
    ) -> list[list[float]]: ...

    @abstractmethod
    def chat(self, model_size: str, instructions: str, messages: list): ...

    @abstractmethod
    def struct_output(
        self, model_size: str, instructions: str, messages: list, structure: BaseModel
    ): ...

    @abstractmethod
    def func_call(self, model_size: str, instructions: str, messages: list, func): ...

    @abstractmethod
    def text_to_speech(self, model_size: str, text: str): ...

    @abstractmethod
    def speech_to_text(self, model_size: str, speech_path: str): ...
