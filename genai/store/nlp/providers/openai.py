import os
import re
from uuid import uuid4
from openai import OpenAI
from ..interface import BaseNLP


class OpenAINLP(BaseNLP):
    def __init__(self, settings):
        self.settings = settings
        self.openai_client = None

    def connect(self):
        self.openai_client = OpenAI(api_key=self.settings.OPENAI_API_KEY)

    def disconnect(self):
        self.openai_client.close()

    def embed(self, queries, batch_size=100, model_name="text-embedding-3-large"):
        embeddings = list()
        for start in range(0, len(queries), batch_size):
            end = start + batch_size
            batch_texts = queries[start:end]
            response = self.openai_client.embeddings.create(
                input=batch_texts,
                model=model_name,
            )
            batch_embeddings = [item.embedding for item in response.data]
            embeddings.extend(batch_embeddings)
        return embeddings

    def chat(self, messages, model_name):
        response = self.openai_client.beta.chat.completions.parse(
            model=model_name, messages=messages, temperature=0.0, top_p=1.0
        )
        msg = response.choices[0].message
        return msg.content

    def structured_output(self, response_model, model_name, messages):
        response = self.openai_client.beta.chat.completions.parse(
            model=model_name,
            messages=messages,
            response_format=response_model,
            temperature=0.0,
            top_p=1.0,
        )
        msg = response.choices[0].message
        return msg.parsed

    def text_to_speech(self, text):
        cleaned_text = re.sub(r"[#*\-]\s?", "", text)
        speech_dir = "/code/server/assets/audio/"
        speech_filename = str(uuid4()) + ".wav"
        speech_file_path = os.path.join(speech_dir, speech_filename)
        os.makedirs(speech_dir, exist_ok=True)

        instructions = """Tone: The voice should be refined, formal, and delightfully theatrical, reminiscent of a charming radio announcer from the early 20th century.\n\nPacing: The speech should flow smoothly at a steady cadence, neither rushed nor sluggish, allowing for clarity and a touch of grandeur.\n\nPronunciation: Words should be enunciated crisply and elegantly, with an emphasis on vintage expressions and a slight flourish on key phrases.\n\nEmotion: The delivery should feel warm, enthusiastic, and welcoming, as if addressing a distinguished audience with utmost politeness.\n\nInflection: Gentle rises and falls in pitch should be used to maintain engagement, adding a playful yet dignified flair to each sentence.\n\nWord Choice: The script should incorporate vintage expressions like splendid, marvelous, posthaste, and ta-ta for now, avoiding modern slang."""
        with self.openai_client.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts",
            voice="alloy",
            input=cleaned_text,
            instructions=instructions,
        ) as response:
            response.stream_to_file(speech_file_path)

        return speech_file_path

    def func_call(self, func, model_name, messages): ...
    def speech_to_text(self, speech_path): ...
