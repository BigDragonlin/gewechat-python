import sqlite3
import time
from ..api.client import GewechatClient
from traceback import print_stack
from ..util.log import logger
from ..util.db import SqliteDB

class SendMessage:
    _instance = None
    def __new__(cls, client:GewechatClient, app_id):
        if cls._instance == None:
            cls._instance = object.__new__(cls)
            cls._instance._initialized = False
            return cls._instance
        return cls._instance
        
    def __init__(self, client:GewechatClient, app_id):
        if not self._initialized:
            self.client = client
            self.app_id = app_id
            #初始化发送者信息
            self.self_profile = client._personal_api.get_profile(app_id)
            #初始化朋友圈
            self.friends_id = []
            self.get_friends()
            self.sqlite_db = SqliteDB()
            self._initialalized = True
            
    def get_friends(self):
        fetch_contacts_list_result = self.client.fetch_contacts_list(self.app_id)
        if fetch_contacts_list_result.get('ret') != 200 or not fetch_contacts_list_result.get('data'):
            logger.error("获取通讯录列表失败: %s", fetch_contacts_list_result)
            return
        friends = fetch_contacts_list_result['data'].get('friends', [])
        if not friends:
            logger.warning("获取到的好友列表为空")
            return
        friends_info = self.client.get_brief_info(self.app_id, friends)
        if friends_info.get('ret') != 200 or not friends_info.get('data'):
            logger.error("获取好友简要信息失败: %s", friends_info)
            return
        friends_info_list = friends_info['data']
        if not friends_info_list:
            logger.warning("获取到的好友简要信息列表为空")
            return
        for friend_info in friends_info_list:
                wxid = friend_info.get('userName')
                self.friends_id.append(wxid)
    def send_msg_by_wxid(self, wx_id, message):
        app_id = self.app_id
        send_msg_result = self.client.post_text(app_id, wx_id, message)
        if send_msg_result.get('ret') != 200:
            logger.error("发送消息失败: %s", send_msg_result)
            return

def run_send_message_server(client: GewechatClient, app_id):
    send_handler = SendMessage(client, app_id)
    sqliteDB = SqliteDB()
    error_time = 0
    while True:
        try:
            messages = sqliteDB.select_answer()
            if messages:
                logger.error(f"添加{send_handler.friends_id},{messages[0][1]}")
                send_handler.send_msg_by_wxid(messages[0][1], messages[0][2])
                sqliteDB.delete_answer(messages[0][0])
                logger.error(f"message is {messages}")
            else:
                time.sleep(2)
            
        except Exception as e:
            logger.exception(f"消息处理失败{e}")
            error_time += 1
            if error_time > 20:
                break
            time.sleep(3)
            continue

def send_msg(client, app_id):
    send_msg_nickname = "林木"  # 要发送消息的好友昵称
    # 获取好友列表
    fetch_contacts_list_result = client.fetch_contacts_list(app_id)
    if fetch_contacts_list_result.get('ret') != 200 or not fetch_contacts_list_result.get('data'):
        logger.error("获取通讯录列表失败: %s", fetch_contacts_list_result)
        return
    # {'ret': 200, 'msg': '操作成功', 'data': {'friends': ['weixin', 'fmessage', 'medianote', le', 'wxid_abcxx'], 'chatrooms': ['1234xx@chatroom'], 'ghs': ['gh_xx']}}
    friends = fetch_contacts_list_result['data'].get('friends', [])
    if not friends:
        logger.warning("获取到的好友列表为空")
        return

    # 获取好友的简要信息
    friends_info = client.get_brief_info(app_id, friends)
    if friends_info.get('ret') != 200 or not friends_info.get('data'):
        logger.error("获取好友简要信息失败: %s", friends_info)
        return
    # 找对目标好友的wxid
    friends_info_list = friends_info['data']
    if not friends_info_list:
        logger.warning("获取到的好友简要信息列表为空")
        return
    wxid = None
    for friend_info in friends_info_list:
        if friend_info.get('nickName') == send_msg_nickname:
            wxid = friend_info.get('userName')
            break
    if not wxid:
        logger.error("没有找到好友: %s 的wxid", send_msg_nickname)
        return

    # 发送消息
    send_msg_result = client.post_text(app_id, wxid, "你好啊")
    if send_msg_result.get('ret') != 200:
        logger.error("发送消息失败: %s", send_msg_result)
        return
    logger.info("发送消息成功: %s", send_msg_result)
    return True
