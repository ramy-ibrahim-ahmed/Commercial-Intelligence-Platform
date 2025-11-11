from typing import Literal
from .interface import BaseNLP
from .providers import OpenAINLP, GeminiNLP


class NLPFactory:
    def __init__(self, settings):
        self.settings = settings

    def create(self, provider: Literal["gemini", "openai"]):
        if provider.lower() == "gemini":
            return GeminiNLP(settings=self.settings)

        elif provider.lower() == "openai":
            return OpenAINLP(settings=self.settings)

        else:
            raise ValueError(f"Not available provider: {provider}")
