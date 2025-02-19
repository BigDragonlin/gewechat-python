import unittest
import json
import requests
from gewechat_client.util.dify import Dify
from gewechat_client.util.config import config

class TestDifyAPI(unittest.TestCase):
    def setUp(self):
        self.url = "https://api.dify.ai/v1/completion-messages"
        self.headers = {
            'Authorization': 'Bearer app-d3VRFwb42JXy3i7GbG4YIGuz',
            'Content-Type': 'application/json',
        }

    def test_dify_api(self):
        data = {
            "inputs": {
                "user_zodiac": "摩羯座",
                "today_date": "2021-09-01"
            },
            "response_mode": "blocking",
            "user": "abc-123",
        }
        response = requests.post(
            self.url, 
            headers=self.headers,
            data=json.dumps(data))
        # print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        print(response.json())
        
    def test_class_dify(self):
        base_url = config["dify"]["api_url"]
        api_key = config["dify"]["fortone_teller"]["api_key"]
        api_type = config["dify"]["fortone_teller"]["api_type"]
        dify = Dify(base_url, api_type, api_key)
        data = {
            "inputs": {
                "user_zodiac": "摩羯座",
                "today_date": "2021-09-01"
            },
            "response_mode": "blocking",
            "user": "abc-123",
        }
        response = dify.get_response(data)
        # print(response)
    
    def test_class_dify_error(self):
        base_url = config["dify"]["api_url"]
        api_key = config["dify"]["fortone_teller"]["api_key"]
        api_type = config["dify"]["fortone_teller"]["api_type"]
        dify = Dify(base_url, api_type, api_key)
        data = {
            "inputs": {
                "user_zodiac": "摩羯座",
                "today_date": "2021-09-01"
            },
            "response_mode": "error",
            "user": "abc-123",
        }
        with self.assertRaises(RuntimeError):
            dify.get_response(data)


if __name__ == '__main__':
    unittest.main()
