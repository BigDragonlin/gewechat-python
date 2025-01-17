import json
import sqlite3

class PersonalMessageHandler:
    def __init__(self):
        # 判断有没有私聊数据库，没有就创建
        self.conn = sqlite3.connect('messages.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_messages (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender TEXT NOT NULL,
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
                self.save_message(sender, message)
            else:
                print("Error: Invalid format for 'PushContentStr'.")
        else:
            print("Error: 'PushContent' is not equal to 1 or is not an integer.")

    def save_message(self,data):
        user_id = data["user_id"]
        name = data["name"]
        age = data["age"]
        # 保存私聊消息到数据库
        self.cursor.execute('''
                            INSERT INTO user_message (id, name, age) VALUES (?, ?, ?)
        ''', (user_id, name, age))
        self.conn.commit()


def personal_message_handler(data):
    # 检查 'Data' 键是否存在
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
        else:
            print("Error: Invalid format for 'PushContentStr'.")
    else:
        print("Error: 'PushContent' is not equal to 1 or is not an integer.")
