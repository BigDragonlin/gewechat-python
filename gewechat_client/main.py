import threading
import os
from .receive_message.callbackhandler import run_callback_server
from .send_message.sendmessage import *
from .api.client import GewechatClient
from .util.config import config

def main():
    # 配置参数
    base_url = config["gewe"]["base_url"]
    callback_url = config["gewe"]["callback_url"]
    port = config["gewe"]["callback_port"]
    app_id = config["gewe"]["app_id"]  

    # 创建 GewechatClient 实例
    client = GewechatClient(base_url)
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
            callback_thread = threading.Thread(target=run_callback_server, args=(callback_url, port))
            callback_thread.start()

            #设置一个新进程，监听队列中的消息，并发送到微信
            callback_listener_thread = threading.Thread(target=run_send_message_server, args=(client, app_id))
            callback_listener_thread.start()

            client.set_callback(client._login_api.token, callback_url)
    except Exception as e:
        print("Failed to fetch contacts list:", str(e))

if __name__ == "__main__":
    main()