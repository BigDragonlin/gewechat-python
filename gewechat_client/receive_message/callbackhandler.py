import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from .receive_personal_message import personal_message_handler 
from ..util.log import logger  # 引入日志库

class CallbackHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/bot/receive/":
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"ret": 404, "msg": "路径未找到"}
            self.wfile.write(json.dumps(response).encode('utf-8'))
            return
    
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"ret": 200, "msg": "消息接收成功"}
            self.wfile.write(json.dumps(response).encode('utf-8'))
            personal_message_handler(data)
        except json.JSONDecodeError:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"ret": 400, "msg": "无效的 JSON 数据"}
            self.wfile.write(json.dumps(response).encode('utf-8'))
            logger.error("无效的 JSON 数据: %s", post_data)

    def do_GET(self):
        logger.info("收到 GET 请求")
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {"ret": 200, "msg": "GET request received"}
        self.wfile.write(json.dumps(response).encode('utf-8'))
def run_callback_server(callback_url, port):
    logger.info("run_callback_server %s %s", callback_url, port)
    callback_url = "0.0.0.0"
    server_address = (callback_url, port)
    logger.info("server_address %s", server_address)
    httpd = HTTPServer(server_address, CallbackHandler)
    logger.info("回调服务器正在运行，监听端口 %s...", port)
    httpd.serve_forever()
