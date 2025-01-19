from gewechat_client import GewechatClient
from callbackhandler import run_callback_server
from send_message.sendmessage import *
import threading
import os
import queue

# 创建消息队列
message_queue = queue.Queue()

def main():
    # 配置参数
    # base_url = os.environ.get("BASE_URL", "http://10.244.148.75:2531/v2/api")
    base_url = os.environ.get("BASE_URL", "http://127.0.0.1:2531/v2/api")
    # 回调函数
    callback_url = "http://host.docker.internal:9912/bot/receive/"
    token = ""
    # app_id = os.environ.get("APP_ID", "xxx")
    app_id = "wx_eK2IMGLgJyvVz7yPPN7ao"
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
        # 给发一条信息确认登录成功
        send_msg_error = send_msg(client, app_id)
        if not send_msg_error:
            print("发送消息失败")
            return
        else:
            #传入回调函数
            #在新进程中启用回调
            callback_thread = threading.Thread(target=run_callback_server, args=(callback_url, port))
            callback_thread.start()

            #设置一个新进程，监听队列中的消息，并发送到微信
            callback_listener_thread = threading.Thread(target=run_send_message_server, args=(client, app_id, message_queue,))
            callback_listener_thread.start()

            client.set_callback(client._login_api.token, callback_url)
    except Exception as e:
        print("Failed to fetch contacts list:", str(e))

if __name__ == "__main__":
    main()