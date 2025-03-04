import unittest
from unittest.mock import patch, MagicMock
from src.gewechat.utils.http_util import post_json

class TestHttpUtil(unittest.TestCase):
    
    @patch('src.gewechat.utils.http_util.requests.post')
    def test_post_json_success(self, mock_post):
        # 设置模拟响应
        mock_response = MagicMock()
        mock_response.json.return_value = {'ret': 200, 'data': 'test_data'}
        mock_post.return_value = mock_response
        
        # 调用被测试的函数
        base_url = 'http://example.com'
        route = '/api/test'
        token = 'test_token'
        data = {'key': 'value'}
        
        result = post_json(base_url, route, token, data)
        
        # 验证请求参数
        mock_post.assert_called_once_with(
            'http://example.com/api/test',
            json=data,
            headers={
                'Content-Type': 'application/json',
                'X-GEWE-TOKEN': token
            },
            timeout=60
        )
        
        # 验证结果
        self.assertEqual(result, {'ret': 200, 'data': 'test_data'})
    
    @patch('src.gewechat.utils.http_util.requests.post')
    def test_post_json_without_token(self, mock_post):
        # 设置模拟响应
        mock_response = MagicMock()
        mock_response.json.return_value = {'ret': 200, 'data': 'test_data'}
        mock_post.return_value = mock_response
        
        # 调用被测试的函数，不传token
        base_url = 'http://example.com'
        route = '/api/test'
        token = None
        data = {'key': 'value'}
        
        result = post_json(base_url, route, token, data)
        
        # 验证请求参数，确认没有token头
        mock_post.assert_called_once_with(
            'http://example.com/api/test',
            json=data,
            headers={'Content-Type': 'application/json'},
            timeout=60
        )
        
        # 验证结果
        self.assertEqual(result, {'ret': 200, 'data': 'test_data'})
    
    @patch('src.gewechat.utils.http_util.requests.post')
    def test_post_json_error_response(self, mock_post):
        # 设置模拟响应
        mock_response = MagicMock()
        mock_response.json.return_value = {'ret': 400, 'message': 'Bad Request'}
        mock_post.return_value = mock_response
        mock_response.text = '{"ret": 400, "message": "Bad Request"}'
        
        # 调用被测试的函数
        base_url = 'http://example.com'
        route = '/api/test'
        token = 'test_token'
        data = {'key': 'value'}
        
        # 验证抛出异常
        with self.assertRaises(RuntimeError):
            post_json(base_url, route, token, data)
    
    @patch('src.gewechat.utils.http_util.requests.post')
    def test_post_json_request_exception(self, mock_post):
        # 设置模拟响应抛出异常
        mock_post.side_effect = Exception("Connection error")
        
        # 调用被测试的函数
        base_url = 'http://example.com'
        route = '/api/test'
        token = 'test_token'
        data = {'key': 'value'}
        
        # 验证抛出异常
        with self.assertRaises(RuntimeError):
            post_json(base_url, route, token, data)

if __name__ == '__main__':
    unittest.main() 