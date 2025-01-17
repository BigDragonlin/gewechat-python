from gewechat_client import GewechatClient
from callbackhandler import run_callback_server
import threading
import os

def main():
    # 配置参数
    # base_url = os.environ.get("BASE_URL", "http://10.244.148.75:2531/v2/api")
    base_url = os.environ.get("BASE_URL", "http://127.0.0.1:2531/v2/api")
    # 回调函数
    callback_url = "http://host.docker.internal:9912/bot/receive/"
    token = ""
    # app_id = os.environ.get("APP_ID", "xxx")
    app_id = "wx_mKqJB4PYbvELd5op2PwkM"
    # 回调函数端口
    port = 9912

    # 创建 GewechatClient 实例
    client = GewechatClient(base_url, token)
    # 登录, 自动创建二维码，扫码后自动登录
    app_id, error_msg = client.login(app_id=app_id)
    if error_msg:
        print("登录失败")
        return
    try:
        #传入回调函数
        #在新进程中启用回调
        callback_thread = threading.Thread(target=run_callback_server, args=(callback_url, port))
        callback_thread.start()
        
        callback_state = client.set_callback(client._login_api.token, callback_url)
        print("设置回调", callback_state)
    except Exception as e:
        print("Failed to fetch contacts list:", str(e))

if __name__ == "__main__":
    main()