import unittest
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request

class SimpleThreadedHandler(BaseHTTPRequestHandler):
    """一个简单的线程化请求处理类"""
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Hello from threaded server!")
        print("Received GET request")

def run_threaded_server(port, handler_class, server_shutdown_event):
    """
    使用线程运行服务器，允许并发处理请求。
    使用 server_shutdown_event 控制服务器生命周期。
    """
    server_address = ('localhost', port)
    httpd = HTTPServer(server_address, handler_class)
    server_shutdown_event.clear() # 确保事件是未设置状态
    while not server_shutdown_event.is_set():
        httpd.handle_request() # 循环处理请求，但不再是 serve_forever
    httpd.server_close()

class TestSimpleThreadedHTTPServer(unittest.TestCase):

    SERVER_PORT = 8090
    server_shutdown_event = threading.Event()

    @classmethod
    def setUpClass(cls):
        """在所有测试开始前，在后台线程启动服务器"""
        cls.server_thread = threading.Thread(
            target=run_threaded_server,
            args=(cls.SERVER_PORT, SimpleThreadedHandler, cls.server_shutdown_event),
            daemon=True # 守护线程
        )
        cls.server_thread.start()
        time.sleep(0.5) # 等待服务器启动

    @classmethod
    def tearDownClass(cls):
        """在所有测试结束后，关闭服务器线程"""
        cls.server_shutdown_event.set() # 发出服务器关闭信号
        cls.server_thread.join(timeout=1) # 等待线程结束

    def test_threaded_get_request(self):
        """测试线程化服务器的 GET 请求"""
        url = f"http://localhost:{self.SERVER_PORT}"
        with urllib.request.urlopen(url) as response:
            self.assertEqual(response.getcode(), 200)
            response_body = response.read().decode('utf-8')
            self.assertEqual(response_body, "Hello from threaded server!")

if __name__ == '__main__':
    unittest.main()