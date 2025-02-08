import unittest
from gewechat_client.util.config import config
from gewechat_client.util.ai import ai

class TestDeepSeekClient(unittest.TestCase):
    def setUp(self):
        api_key = config["ai"]["api_key"]
        print("api_key:", api_key)
        self.client = ai(api_key)
        
    def test_get_response(self):
        model = config["ai"]["model_level_3"]
        user_message = "你好"
        system_prompt = "你是一个助手"
        response = self.client.get_response(model, user_message, system_prompt)
        print("response:", response)
        self.assertIsNotNone(response)