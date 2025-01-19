import json
import sqlite3
from ..ai import *
from .. import main

class PersonalMessageHandler:
    def __init__(self):
        # 初始化数据库
        self.init_database()
        # 初始化openid
        self.ai = ai("sk-4d28ca4e4e3c41d7ba35b57629dd72b1")
        
    def init_database(self):
        self.conn = sqlite3.connect('messages.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                message TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def handle_message(self, data):
        # 处理私聊消息
        if "Data" not in data:
            print("Error: 'Data' key is missing in the input data.")
            return
        # 获取 'PushContent'
        push_content = data["Data"].get("MsgType")
        # 检查 'PushContent' 是否为预期类型
        if isinstance(push_content, int) and push_content == 1:
            push_content_str = data["Data"].get("PushContent")  # 假设 PushContentStr 是消息内容的键
            if push_content_str and " : " in push_content_str:
                sender, message = push_content_str.split(" : ", 1)
                print(f"发送者: {sender}")
                print(f"发送内容: {message}")
                sender_wxid = data["Data"].get("FromUserName").get("string")
                self.save_message({"name": sender, "message": message})
                self.process_message(sender, message, sender_wxid)
            else:
                print("Error: Invalid format for 'PushContentStr'.")
        else:
            print("Error: 'PushContent' is not equal to 1 or is not an integer.")

    def save_message(self, data):
        name = data["name"]
        message = data["message"]
        # 保存私聊消息到数据库
        self.cursor.execute("INSERT INTO user_messages (name, message) VALUES (?, ?)", (name, message))
        self.conn.commit()

    def process_message(self, sender, message, sender_wxid):
        # 获取本用户所有消息,根据时间戳排序
        # 获取用户信息,接入ai,帮我
        response = self.ai.get_response(message)
        # 根据时间戳排序
        # 讲回答放入消息队列
        main.message_queue.put({sender_wxid: response})

def personal_message_handler(data):
    # 检查 'Data' 键是否存在
    if "Data" not in data:
        print("Error: 'Data' key is missing in the input data.")
        return
    # 获取 'PushContent'
    push_content = data["Data"].get("MsgType")

    # 检查 'PushContent' 是否为预期类型
    if isinstance(push_content, int) and push_content == 1:
        handler_msg = PersonalMessageHandler()
        handler_msg.handle_message(data)
    else:
        print("Error: Invalid format for 'PushContentStr'.")

