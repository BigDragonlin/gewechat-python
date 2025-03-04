import unittest
from unittest.mock import patch, MagicMock
import json
import requests
from src.gewechat.utils.dify import Dify

class TestDify(unittest.TestCase):
    
    def setUp(self):
        # 设置测试数据
        self.api_url = "https://api.dify.ai"
        self.api_type = "/v1/completion-messages"
        self.api_key = "test_api_key"
        self.dify = Dify(self.api_url, self.api_type, self.api_key)
    
    def test_init(self):
        # 测试初始化
        self.assertEqual(self.dify.api_url, "https://api.dify.ai/v1/completion-messages")
        self.assertEqual(self.dify.api_key, "test_api_key")
        self.assertEqual(self.dify.headers, {
            "Content-Type": "application/json",
            "Authorization": "Bearer test_api_key"
        })
    
    def test_init_with_trailing_slash(self):
        # 测试带有尾部斜杠的URL初始化
        dify = Dify("https://api.dify.ai/", "/v1/completion-messages", self.api_key)
        self.assertEqual(dify.api_url, "https://api.dify.ai/v1/completion-messages")
    
    @patch('requests.post')
    def test_get_response_success(self, mock_post):
        # 设置模拟响应
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"answer": "测试回答"}
        mock_post.return_value = mock_response
        
        # 调用被测试的方法
        data = {"inputs": {"query": "测试问题"}}
        result = self.dify.get_response(data)
        
        # 验证请求参数
        mock_post.assert_called_once_with(
            "https://api.dify.ai/v1/completion-messages",
            headers=self.dify.headers,
            data=json.dumps(data)
        )
        
        # 验证结果
        self.assertEqual(result, {"answer": "测试回答"})
    
    @patch('requests.post')
    def test_get_response_error(self, mock_post):
        # 设置模拟响应
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request"
        mock_post.return_value = mock_response
        
        # 调用被测试的方法并验证异常
        data = {"inputs": {"query": "测试问题"}}
        with self.assertRaises(RuntimeError) as context:
            self.dify.get_response(data)
        
        # 验证异常消息
        self.assertEqual(str(context.exception), "Bad Request")
    
    @patch('requests.post')
    def test_get_response_network_error(self, mock_post):
        # 设置模拟响应抛出网络异常
        mock_post.side_effect = requests.exceptions.ConnectionError("Connection refused")
        
        # 调用被测试的方法并验证异常
        data = {"inputs": {"query": "测试问题"}}
        with self.assertRaises(requests.exceptions.ConnectionError):
            self.dify.get_response(data)

if __name__ == '__main__':
    unittest.main() 