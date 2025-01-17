from openai import OpenAI
import unittest
from unittest.mock import MagicMock

class DeepSeekClient:
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

class TestDeepSeekClient(unittest.TestCase):
    def setUp(self):
        # 模拟 OpenAI 客户端
        self.mock_client = MagicMock()
        self.deepseek_client = DeepSeekClient(api_key="sk-4d28ca4e4e3c41d7ba35b57629dd72b1")
        self.deepseek_client.client = self.mock_client

    # def test_get_response(self):
    #     # 模拟 API 响应
    #     mock_response = MagicMock()
    #     mock_response.choices = [MagicMock()]
    #     mock_response.choices[0].message = MagicMock()
    #     mock_response.choices[0].message.content = "Hello, how can I help you?"

    #     self.mock_client.chat.completions.create.return_value = mock_response

    #     # 调用方法并断言结果
    #     response = self.deepseek_client.get_response("Hello")
    #     print("回答：")
    #     print(response)
    #     self.assertEqual(response, "Hello, how can I help you?")
    #     self.mock_client.chat.completions.create.assert_called_once_with(
    #         model="deepseek-chat",
    #         messages=[
    #             {"role": "system", "content": "You are a helpful assistant"},
    #             {"role": "user", "content": "Hello"},
    #         ],
    #         stream=False
    #     )
        
    def test_real_response(self):

        # 替换为你的 DeepSeek API Key
        api_key = "sk-4d28ca4e4e3c41d7ba35b57629dd72b1"

        # 创建 OpenAI 客户端
        client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

        # 向 DeepSeek 提问
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": "Python 中如何创建一个简单的 HTTP 服务器？"},
            ],
            stream=False
        )
        print("打印回答")
        # 打印模型的回答
        print(response.choices[0].message.content)


if __name__ == '__main__':
    unittest.main()