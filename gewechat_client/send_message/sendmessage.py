import sqlite3
import time
from ..api.client import GewechatClient
from traceback import print_stack
from ..util.log import logger  # 引入日志库

class SendMessage:
    def __init__(self, client:GewechatClient, app_id):
        database = "messages.db"
        table_name = "answer_queue_personal"
        self.client = client
        self.app_id = app_id
        #初始化sqlite个人消息队列
        self.init_database_personal_queue(database, table_name)
        #初始化发送者信息
        self.self_profile = client._personal_api.get_profile(app_id)
    
    def init_database_personal_queue(self, database, table_name):
        #初始化个人消息队列
        self.conn = sqlite3.connect(database)
        self.cursor = self.conn.cursor()
        self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                wx_id TEXT PRIMARY KEY,
                message TEXT
            )
        """)
        self.conn.commit()
            
    def select_database_personal_by_wx_id(self):
        self.cursor.execute('SELECT * FROM answer_queue_personal')
        result = self.cursor.fetchall()
        if result:
            return result
        else:
            return None

    def send_msg_by_wxid(self, wx_id, message):
        app_id = self.app_id
        send_msg_result = self.client.post_text(app_id, wx_id, message)
        if send_msg_result.get('ret') != 200:
            logger.error("发送消息失败: %s", send_msg_result)
            return

def run_send_message_server(client: GewechatClient, app_id):
    send_handler = SendMessage(client, app_id)
    send_wx_id = send_handler.self_profile["data"]["wxid"]
    while True:
        try:
            with sqlite3.connect("messages.db") as conn:
                cursor = conn.cursor()
                messages = cursor.execute('SELECT * FROM answer_queue_personal').fetchall()
                if messages:
                    conn.execute("BEGIN TRANSACTION")
                    try:
                        for message in messages:
                            if message[1]:
                                send_handler.send_msg_by_wxid(message[0], message[1])
                                cursor.execute('INSERT INTO user_messages (wx_id, message) VALUES (?, ?)',(send_wx_id, message[1]))
                            cursor.execute('DELETE FROM answer_queue_personal WHERE wx_id=?', (message[0],))
                            conn.commit()
                    except Exception as e:
                        logger.exception("事务处理失败")
                        conn.rollback()
                        continue
        except Exception as e:
            logger.exception("消息处理失败")
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
