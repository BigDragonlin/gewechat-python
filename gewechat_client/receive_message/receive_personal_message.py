import sqlite3
from ..util.ai import *
from ..util.config import config
from ..util.log import logger

class PersonalMessageHandler:
    def __init__(self):
        # 初始化数据库
        self.init_database()
        # 初始化openid
        self.ai = ai(config["ai"]["api_key"])
        
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
        
        # 初始化打卡数据库，包括打卡人wx_id,打卡内容，时间戳
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS checkin_data (
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
        return "你好"
        # wx_id = data["wx_id"]
        # message = data["message"]
        # print("回答", data)
        # if message == "":
        #     return
        #  # 检查是否已存在该 wx_id
        # logger.info("回答", wx_id, message)
        # self.cursor.execute("INSERT INTO answer_queue_personal (wx_id, message) VALUES (?, ?)", (wx_id, message))
        # self.conn.commit()
        pass
        
    def handle_message(self, data):
        if "Data" not in data:
            logger.error("Error: 'Data' key is missing in the input data.")
            return
        message_type = data["Data"].get("Wxid")
        # 如果message_type以@chatroom结尾，则是群聊消息
        if message_type.endswith("@chatroom"):
            self.handle_group_message(data)
        push_content = data["Data"].get("MsgType")
        #文字消息
        if isinstance(push_content, int) and push_content == 1:
            push_content_str = data["Data"].get("PushContent")   
            if push_content_str and " : " in push_content_str:
                _, message = push_content_str.split(" : ", 1)
                sender_wx_id = data["Data"].get("FromUserName").get("string")
                logger.info("接收消息", sender_wx_id, message)
                self.save_message({"sender_wx_id": sender_wx_id, "message": message})
                self.process_message(message, sender_wx_id, data)
            else:
                logger.error("Error: Invalid format for 'PushContentStr'.")
        else:
            logger.error("Error: 'PushContent' is not equal to 1 or is not an integer.")

    def process_message(self, message, sender_wx_id, data):
        # 判断message是不是@help, 如果是则返回帮助信息
        response = ""
        if message.startswith("@help"):
            response = "你可以发送以下命令：\n\n" \
                       "@help：查看帮助信息\n" \
                       "@clear：清除历史记录\n" \
                       "@reset：重置对话\n" \
                       "@exit：退出对话\n" \
                       "@exitall：退出所有对话\n" \
                       "@clearall：清除所有对话记录\n"
        elif message.startswith("@开启"):
            pass
        elif sender_wx_id == "39292796878@chatroom":
            response = self.process_879chatroom(message, data)
        else:
            response = self.ai.get_response(config["ai"]["model_level_2"],message, "你是一个私人助理，回答我的问题，最好每句回答要带上表情符号")
        self.save_answer({"wx_id": sender_wx_id, "message": response})

    #处理读书群消息
    def process_879chatroom(self, message, data):
        print("message 测试", message)
        print("data 数据", data)
        # #判断是不是打卡消息,"deepseek-reasoner"
        # check_is_checkin = self.ai.get_response("deepseek-chat", message, "你是一个读书打卡群的机器人，判断消息是否是读书分享内容,如果是打卡消息请返回true，如果不是打卡消息，请返回false。")
        # #如果是打卡消息，将打卡数据存到数据库中。并回复打卡成功
        # if check_is_checkin == "true":
        #     send_message_wx_id = data["Data"].get("Content").get("string").split(':\n', 1)[0]
        #     self.save_checkin_data(send_message_wx_id, message)
        #     print(send_message_wx_id, "打卡成功")
        # else:
        #     print("check info", check_is_checkin)
        return "你好呀"
            
    #插入打卡信息到打卡数据库
    def save_checkin_data(self, wx_id, message):
        # 检查今天是否已有该用户的打卡记录
        self.cursor.execute(
            "SELECT 1 FROM checkin_data "
            "WHERE wx_id=? AND DATE(timestamp) = DATE('now') "
            "LIMIT 1",
            (wx_id,)
        )
        if self.cursor.fetchone():
            print("Error: User has already checked in today.")
            return
        self.cursor.execute("INSERT INTO checkin_data (wx_id, message) VALUES (?, ?)", (wx_id, message))
        self.conn.commit()
            
def personal_message_handler(data):
    # 检查 'Data' 键是否存在
    if "Data" not in data:
        print("Error: 'Data' key is missing in the input data.")
        return
    PersonalMessageHandler().handle_message(data)
