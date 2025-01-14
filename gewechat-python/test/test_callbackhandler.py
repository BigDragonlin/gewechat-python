import unittest
import threading
import time
import json
import http.client

class TestCallbackServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 启动回调服务器
        cls.server_thread = threading.Thread(target=run_callback_server, daemon=True)
        cls.server_thread.start()
        time.sleep(1)  # 等待服务器启动

    def test_callback_handler(self):
        # 模拟发送 POST 请求
        conn = http.client.HTTPConnection("localhost", 8080)
        headers = {'Content-type': 'application/json'}
        data = {"message": "Hello, World!"}
        json_data = json.dumps(data)

        # 发送请求
        conn.request("POST", "/callback", body=json_data, headers=headers)
        response = conn.getresponse()

        # 验证响应状态码
        self.assertEqual(response.status, 200)

        # 验证响应内容
        response_data = json.loads(response.read().decode('utf-8'))
        self.assertEqual(response_data["ret"], 200)
        self.assertEqual(response_data["msg"], "消息接收成功")

    @classmethod
    def tearDownClass(cls):
        # 停止回调服务器
        cls.server_thread.join(timeout=1)

if __name__ == "__main__":
    unittest.main()