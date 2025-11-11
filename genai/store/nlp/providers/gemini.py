import google.generativeai as genai
from ..interface import BaseNLP
from ....core import GeminiChat, GeminiModel


class GeminiNLP(BaseNLP):
    def __init__(self, settings: genai):
        self.settings = settings
        self.client: genai = None

    def _get_model_name(self, model_size: str):
        if model_size.upper() == GeminiModel.SMALL.name:
            return GeminiModel.SMALL.value
        elif model_size.upper() == GeminiModel.LARGE.name:
            return GeminiModel.LARGE.value

    def connect(self):
        genai.configure(api_key=self.settings.GEMINI_API_KEY)
        self.client = genai

    def create_user_message(self, user_message):
        return {
            GeminiChat.ROLE.value: GeminiChat.USER.value,
            GeminiChat.CONTENT.value: user_message,
        }

    def create_model_message(self, model_message):
        return {
            GeminiChat.ROLE.value: GeminiChat.ASSISTANT.value,
            GeminiChat.CONTENT.value: model_message,
        }

    def embed(
        self,
        queries,
        batch_size=10,
        model_name="gemini-embedding-001",
        task: str = "SEMANTIC_SIMILARITY",
    ):
        embeddings = []
        for i in range(0, len(queries), batch_size):
            batch = queries[i : i + batch_size]
            batch_embeddings = genai.embed_content(
                model=model_name,
                content=batch,
                task_type=task,
            )
            embeddings.extend([e for e in batch_embeddings["embedding"]])
        return embeddings

    def chat(self, model_size, instructions, messages):
        model_name = self._get_model_name(model_size)
        model = self.client.GenerativeModel(
            model_name=model_name, system_instruction=instructions
        )
        response = model.generate_content(messages)
        return response.text

    def struct_output(self, model_size, instructions, messages, structure):
        model_name = self._get_model_name(model_size)
        model = self.client.GenerativeModel(
            model_name=model_name, system_instruction=instructions
        )
        response = model.generate_content(
            contents=messages,
            generation_config={
                "response_mime_type": "application/json",
                "response_schema": structure,
            },
        )
        return structure.model_validate_json(response.text)

    def func_call(self, model_size, messages, instructions, func):
        model_name = self._get_model_name(model_size)
        model = self.client.GenerativeModel(
            model_name=model_name, system_instruction=instructions
        )
        try:
            response = model.generate_content(messages, tools=[func])
            call = response.candidates[0].content.parts[0].function_call

            if call:
                try:
                    result = func(**call.args)
                    return result
                except Exception as e:
                    args_dict = dict(call.args)
                    return f"Error when calling {call.name} with args {args_dict}: {e}"

        except Exception as e:
            return f"Error during model generation: {e}"

        return None

    def speech_to_text(self, model_name, speech_path):
        myfile = self.client.upload_file(path=speech_path)
        model = self.client.GenerativeModel(model_name)
        response = model.generate_content(
            contents=["Generate a transcript of the speech.", myfile],
        )
        return response.text

    def text_to_speech(self, model_name, text):
        model = self.client.GenerativeModel(model_name)
        generation_config = {
            "response_modalities": ["AUDIO"],
            "speech_config": {
                "voice_config": {
                    "prebuilt_voice_config": {
                        "voice_name": self.settings.GEMINI_VOICE_NAME
                    }
                }
            },
        }

        response = model.generate_content(
            contents=[text],
            generation_config=generation_config,
        )

        for part in response.candidates[0].content.parts:
            inline = getattr(part, "inline_data", None)
            if inline and getattr(inline, "data", None):
                return inline.data

        raise RuntimeError("No audio inline_data found in response")

    def disconnect(self): ...
