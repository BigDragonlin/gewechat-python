import requests
import json

class Dify():
    def __init__(self, api_url, api_type, api_key):
        self.api_url = f"{api_url.rstrip('/')}/{api_type.lstrip('/')}"
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
    
    def get_response(self, data):
        response = requests.post(
            self.api_url, 
            headers=self.headers,
            data=json.dumps(data))
        if response.status_code == 200:
            return response.json()
        else:
            raise RuntimeError(response.text)