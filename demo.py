import os
from gewechat_client.api.client import GewechatClient
from gewechat_client.util.config import load_config
from gewechat_client.util.log import logger  # 引入日志库

def main():
    # 配置参数
    config = load_config()
    base_url = config["gewe"]["base_url"]
    app_id = config["gewe"]["app_id"]
    send_msg_nickname = "林木" # 要发送消息的好友昵称

    # 创建 GewechatClient 实例
    client = GewechatClient(base_url)

    # 登录, 自动创建二维码，扫码后自动登录
    app_id, error_msg = client.login(app_id=app_id)
    if error_msg:
        logger.error("登录失败")
        return
    try:
        fetch_contacts_list_result = client.fetch_contacts_list(app_id)
        if fetch_contacts_list_result.get('ret') != 200 or not fetch_contacts_list_result.get('data'):
            logger.error("获取通讯录列表失败: %s", fetch_contacts_list_result)
            return
        friends = fetch_contacts_list_result['data'].get('friends', [])
        if not friends:
            logger.warning("获取到的好友列表为空")
            return
        logger.info("获取到的好友列表: %s", friends)

        friends_info = client.get_brief_info(app_id, friends)
        if friends_info.get('ret') != 200 or not friends_info.get('data'):
            logger.error("获取好友简要信息失败: %s", friends_info)
            return
        friends_info_list = friends_info['data']
        if not friends_info_list:
            logger.warning("获取到的好友简要信息列表为空")
            return
        wxid = None
        for friend_info in friends_info_list:
            if friend_info.get('nickName') == send_msg_nickname:
                logger.info("找到好友: %s", friend_info)
                wxid = friend_info.get('userName')
                break
        if not wxid:
            logger.error("没有找到好友: %s 的wxid", send_msg_nickname)
            return
        logger.info("找到好友: %s", wxid)

        send_msg_result = client.post_text(app_id, wxid, "你好啊")
        if send_msg_result.get('ret') != 200:
            logger.error("发送消息失败: %s", send_msg_result)
            return
        logger.info("发送消息成功: %s", send_msg_result)
    except Exception as e:
        logger.exception("Failed to fetch contacts list")

if __name__ == "__main__":
    main()
