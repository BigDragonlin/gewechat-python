from openai import OpenAI


class ai:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

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
