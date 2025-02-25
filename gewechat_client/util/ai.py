from openai import OpenAI
from .config import config

class Ai:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
            cls._instance._initialized = False
            return cls._instance
        return cls._instance
    def __init__(self):
        if not self._initialized:
            api_key = config["ai"]["api_key"]
            self.client = OpenAI(api_key=api_key, base_url=config["ai"]["base_url"])
        

    def get_response(self, model, user_message, system_prompt):
        response = self.client.chat.completions.create(
            model = model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            stream=False
        )
        return response.choices[0].message.content