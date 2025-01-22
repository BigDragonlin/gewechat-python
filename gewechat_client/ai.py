from openai import OpenAI


class ai:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    def get_response(self, user_message):
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": user_message},
            ],
            stream=False
        )
        return response.choices[0].message.content
