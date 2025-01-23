import time
import requests
import unittest
from unittest.mock import patch, Mock


# 重试装饰器（用户需要测试的对象）
def retry_on_failure(max_retries=3, delay=1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Attempt {retries+1} failed: {str(e)}")
                    retries += 1
                    time.sleep(delay)
            raise Exception("Max retries exceeded")
        return wrapper
    return decorator

# 使用装饰器的函数
@retry_on_failure(max_retries=3, delay=0.1)
def fetch_data(url):
    response = requests.get(url)
    response.raise_for_status()  # 4xx/5xx 状态码会抛异常
    return response.json()

class TestAPIClient(unittest.TestCase):
    def test_fetch_data(self):
        url = ""
        with patch('requests.get') as mock_get:
            mock_get.return_value.json.return_value = {"data": "test"}
            result = fetch_data(url)
            self.assertEqual(result, {"data": "test"})
            mock_get.assert_called_once_with(url)
            
if __name__ == '__main__':
    unittest.main()