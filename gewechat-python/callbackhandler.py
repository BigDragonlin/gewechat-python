from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class CallbackHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # 读取请求体
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        # 解析 JSON 数据
        try:
            data = json.loads(post_data.decode('utf-8'))
            print("收到回调消息:", data)
            
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

def run_callback_server(port=8080):
    server_address = ('', port)
    httpd = HTTPServer(server_address, CallbackHandler)
    print(f"回调服务器正在运行，监听端口 {port}...")
    httpd.serve_forever()