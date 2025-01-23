import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from receive_message.receive_personal_message import personal_message_handler 

class CallbackHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/bot/receive/":
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"ret": 404, "msg": "路径未找到"}
            self.wfile.write(json.dumps(response).encode('utf-8'))
            return
    
        # 读取请求
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        # 解析 JSON 数据
        try:
            data = json.loads(post_data.decode('utf-8'))
            #处理返回数据
            personal_message_handler(data)
            
            # 返回成功响应
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"ret": 200, "msg": "消息接收成功"}
            self.wfile.write(json.dumps(response).encode('utf-8'))
        except json.JSONDecodeError:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"ret": 400, "msg": "无效的 JSON 数据"}
            self.wfile.write(json.dumps(response).encode('utf-8'))

    def do_GET(self):
        print("收到 GET 请求")
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {"ret": 200, "msg": "GET request received"}
        self.wfile.write(json.dumps(response).encode('utf-8'))
def run_callback_server(callback_url, port):
    print("run_callback_server", callback_url, port)
    callback_url = "0.0.0.0"
    server_address = (callback_url, port)
    print("server_address", server_address)
    httpd = HTTPServer(server_address, CallbackHandler)
    print(f"回调服务器正在运行，监听端口 {port}...")
    httpd.serve_forever()