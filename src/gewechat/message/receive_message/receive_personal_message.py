from src.gewechat.utils.ai import *
from src.gewechat.utils.config import config
from src.gewechat.utils.log import logger
from src.gewechat.utils.db import SqliteDB
from src.gewechat.utils.ai import Ai

class PersonalMessageHandler:
    __instance = None
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
            cls.__instance._initialized = False
            return cls.__instance
        return cls.__instance
    
    def __init__(self):
        if not self._initialized:
            self._initialized = True
            self.sqlite_db = SqliteDB()
            self.ai = Ai()
                
    def handle_message(self, data):
        push_content = data["Data"].get("MsgType")
        #文字消息
        if isinstance(push_content, int) and push_content == 1:
            push_content_str = data["Data"].get("PushContent")   
            if push_content_str and ":" in push_content_str:
                _, message = push_content_str.split(":", 1)
                sender_wx_id = data["Data"].get("FromUserName").get("string")
                self.sqlite_db.save_message(sender_wx_id, message)
                self.process_message(message, sender_wx_id, data)
            else:
                logger.error("Error: Invalid format for 'PushContentStr'.")

    def process_message(self, message, sender_wx_id, data):
        response = ""
        try:
            if message.startswith("@help"):
                response = "你可以发送以下命令：\n\n" \
                        "@help：查看帮助信息\n" \
                        "@clear：清除历史记录\n" \
                        "@reset：重置对话\n" \
                        "@exit：退出对话\n" \
                        "@exitall：退出所有对话\n" \
                        "@clearall：清除所有对话记录\n"
            # else:
            #     ai_level = config["ai"]["model_level_2"]
            #     ai_prompt = "你是一个私人助理，回答我的问题，最好每句回答要带上表情符号"
            #     response = self.ai.get_response(ai_level, message, ai_prompt)
        except Exception as e:
            logger.error("Error occurred: %s", str(e))
            response = f"出现问题，{e}"
        self.sqlite_db.save_answer(sender_wx_id, response)
        logger.info(f"问题：{message}")
        logger.info(f"回答：{response}")
        return response

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