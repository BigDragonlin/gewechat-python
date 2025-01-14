from gewechat_client import GewechatClient
import os
import time

def listen_and_print_messages(client, app_id):
    """
    监听并打印接收到的消息
    :param client: GewechatClient 实例
    :param app_id: 应用的 ID
    """
    try:
        while True:
            # 获取最新消息
            messages = client.fetch_latest_messages(app_id)
            if messages.get('ret') != 200 or not messages.get('data'):
                print("获取消息失败:", messages)
                continue

            # 打印每条消息
            for message in messages['data']:
                sender = message.get('sender')
                content = message.get('content')
                print(f"收到来自 {sender} 的消息: {content}")

            # 每隔一段时间检查一次新消息
            time.sleep(5)  # 5秒检查一次

    except Exception as e:
        print("监听消息失败:", str(e))

def main():
    # 配置参数
    base_url = os.environ.get("BASE_URL", "http://127.0.0.1:2531/v2/api")
    token = ""
    app_id = "wx_8tOrPZFSoywS9s1GfYPpc"

    # 创建 GewechatClient 实例
    client = GewechatClient(base_url, token)

    # 登录, 自动创建二维码，扫码后自动登录
    app_id, error_msg = client.login(app_id=app_id)
    if error_msg:
        print("登录失败")
        return

    # 开始监听并打印消息
    listen_and_print_messages(client, app_id)

if __name__ == "__main__":
    main()