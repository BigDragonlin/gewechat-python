from ..util.ai import *
from ..util.config import config
from ..util.log import logger
from ..util.db import SqliteDB
from ..util.ai import Ai
from ..util.dify import Dify
import re
from datetime import datetime

class GroupMessageHandler:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
            cls._instance._initialized = False
            return cls._instance
        return cls._instance    
    
    def __init__(self):
        if not self._initialized:
            self._initialized = True
            # 初始化数据库和AI实例
            self.sqlite_db = SqliteDB()
            self.ai = Ai()
            self.agent = {}
        
                
    def handle_message(self, data):
        push_content = data["Data"].get("MsgType")
        #文字消息
        if isinstance(push_content, int) and push_content == 1:
            push_content_str = data["Data"].get("Content").get("string")   
            sender_wx_id = data["Data"].get("FromUserName").get("string")
            if push_content_str and ":\n" in push_content_str:
                logger.info(f"push_content_str is {push_content_str}")
                message = re.split(r':\n', push_content_str)
                self.sqlite_db.save_message(sender_wx_id, message[1])
                self.process_message(message[1], sender_wx_id, data)
            else:
                self.sqlite_db.save_message(sender_wx_id, push_content_str)
                self.process_message(message, sender_wx_id, data)
    
    def process_xingzuo(self, xingzuo):
        base_url = config["dify"]["api_url"]
        api_key = config["dify"]["fortone_teller"]["api_key"]
        api_type = config["dify"]["fortone_teller"]["api_type"]
        dify = Dify(base_url, api_type, api_key)
        current_datetime = datetime.now()
        formatted_date = current_datetime.strftime("%Y%m%d") 
        data = {
            "inputs": {
                "user_zodiac": f"{xingzuo}",
                "today_date": f"{formatted_date}"
            },
            "response_mode": "blocking",
            "user": "abc-123",
        }
        try:
            response = dify.get_response(data)
            return response.get("answer")
        except Exception as e:
            logger.error(f"{e}")
        
    def process_lingqian(self):
        base_url = config["dify"]["api_url"]
        api_key = config["dify"]["lingqian"]["api_key"]
        api_type = config["dify"]["lingqian"]["api_type"]
        dify = Dify(base_url, api_type, api_key)
        data = {
            "inputs": {},
            "response_mode": "blocking",
            "user": "abc-123",
        }
        try:
            response = dify.get_response(data)
            response = response["data"]["outputs"]["text"]
            formatted_str = ""
            for key, value in response.items():
                formatted_str += f"{key}：{value}\n"
            return formatted_str
        except Exception as e:
            logger.error(f"{e}")
    
    def process_yunqi(self, xingzuo):
        base_url = config["dify"]["api_url"]
        api_key = config["dify"]["yunqi"]["api_key"]
        api_type = config["dify"]["yunqi"]["api_type"]
        dify = Dify(base_url, api_type, api_key)
        data = {
            "inputs": {
                "xingzuo": f"{xingzuo}",
            },
            "response_mode": "blocking",
            "user": "abc-123",
        }
        try:
            response = dify.get_response(data)
            return response["data"]["outputs"]["result"]
        except Exception as e:
            logger.error(f"{e}")
            return "抱歉，出现错误，请稍后再试。"
    def process_group_at_message(self, message, data):
        logger.info(f"group_at_message:{message}")
        pattern = r'/(.*?)\s(.*?)$'
        match = re.search(pattern, message)
        first_part = match.group(1)
        second_part = match.group(2)
        if first_part == "星座":
            return self.process_xingzuo(second_part)
        elif first_part == "灵签":
            return self.process_lingqian()
        elif first_part == "运气":
            return self.process_yunqi(second_part)
        return ""

    def process_message(self, message, sender_wx_id, data):
        response = ""
        logger.info(f"{sender_wx_id}问题：{message}")
        try:
            if message.startswith("@help"):
                response = "你可以发送以下命令：\n\n" \
                        "@help：查看帮助信息\n" \
                        "/开启 AI：开启AI\n" \
                        "/关闭：关闭agent并清除历史记录\n"
            elif message.startswith("@机器人\u2005"):
                response = self.process_group_at_message(message, data)
            elif message.startswith("/开启"):
                pattern = r'/(.*?)\s(.*?)$'
                match = re.search(pattern, message)
                second_part = match.group(2)
                print(second_part)
                self.agent[sender_wx_id]=second_part
                prompt = "你是一个私人助理，回答我的问题，最好每句回答要带上表情符号"
                self.ai.start_chat_history(sender_wx_id, prompt)
                response = f"开启{second_part}成功"
            elif message.startswith("/关闭"):
                if sender_wx_id in self.agent:
                    del self.agent[sender_wx_id]
                self.ai.stop_chat_history(sender_wx_id)
                response = "关闭成功"
            elif self.agent[sender_wx_id]:
                ai_level = config["ai"]["model_level_1"]
                response = self.ai.get_response_with_history(sender_wx_id, ai_level, "user", message)
            if response == "" or response == None:
                return
            else:
                self.sqlite_db.save_answer(sender_wx_id, response)
            logger.info(f"回答：{response}")
        except Exception as e:
            logger.error("Error occurred: %s", str(e))
            response = f"抱歉,出现错误:{e}。"
    
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