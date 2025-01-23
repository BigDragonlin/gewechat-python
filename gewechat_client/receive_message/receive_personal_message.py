import sqlite3
from idlelib.rpc import response_queue

from gewechat_client.ai import *

class message_handler:
    def __init__(self):
        # 初始化数据库
        self.init_database()
        # 初始化openid
        self.ai = ai("sk-4d28ca4e4e3c41d7ba35b57629dd72b1")
        
    def init_database(self):
        self.conn = sqlite3.connect('messages.db')
        self.cursor = self.conn.cursor()
        # 初始化个人聊天信息库
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                wx_id TEXT NOT NULL,
                message TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()
        
        # 初始化回答队列数据库
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS answer_queue_personal (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                wx_id TEXT NOT NULL,
                message TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()
    def save_message(self, data):
        sender_wx_id = data["sender_wx_id"]
        message = data["message"]
        # 保存私聊消息到数据库
        self.cursor.execute("INSERT INTO user_messages (wx_id, message) VALUES (?, ?)", (sender_wx_id, message))
        self.conn.commit()
    
    def save_answer(self, data):
        wx_id = data["wx_id"]
        message = data["message"]
         # 检查是否已存在该 wx_id
        print("回答", wx_id, message)
        self.cursor.execute("INSERT INTO answer_queue_personal (wx_id, message) VALUES (?, ?)", (wx_id, message))
        self.conn.commit()
        
    def handle_message(self, data):
        if "Data" not in data:
            print("Error: 'Data' key is missing in the input data.")
            return
        push_content = data["Data"].get("MsgType")
        
        #文字消息
        if isinstance(push_content, int) and push_content == 1:
            push_content_str = data["Data"].get("PushContent")  # 假设 PushContentStr 是消息内容的键
            if push_content_str and " : " in push_content_str:
                sender, message = push_content_str.split(" : ", 1)
                sender_wx_id = data["Data"].get("FromUserName").get("string")
                print("接收消息", sender, message)
                self.save_message({"sender_wx_id": sender_wx_id, "message": message})
                self.process_message(message, sender_wx_id)
            else:
                print("Error: Invalid format for 'PushContentStr'.")
        else:
            print("Error: 'PushContent' is not equal to 1 or is not an integer.")

    def process_message(self, message, sender_wx_id):
        # 判断message是不是@help, 如果是则返回帮助信息
        response = ""
        if message.startswith("@help"):
            response = "欢迎使用Gewechat-AI，你可以发送以下命令：\n\n" \
                       "@help：查看帮助信息\n" \
                       "@clear：清除历史记录\n" \
                       "@reset：重置对话\n" \
                       "@exit：退出对话\n" \
                       "@exitall：退出所有对话\n" \
                       "@clearall：清除所有对话记录\n" 
        response = self.ai.get_response(message)
        self.save_answer({"wx_id": sender_wx_id, "message": response})

def personal_message_handler(data):
    # 检查 'Data' 键是否存在
    if "Data" not in data:
        print("Error: 'Data' key is missing in the input data.")
        return
    message_handler().handle_message(data)
