from src.gewechat.utils.log import logger
from src.gewechat.utils.config import config
from openai import OpenAI

class Ai:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
            cls._instance._initialized = False
            return cls._instance
        return cls._instance
    def __init__(self):
        if not self._initialized:
            self.chat_history = {}
            api_key = config["ai"]["api_key"]
            self.client = OpenAI(api_key=api_key, base_url=config["ai"]["base_url"])    
    
    def get_response(self, model, user_message, system_prompt):
        response = self.client.chat.completions.create(
            model = model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            stream=False
        )
        return response.choices[0].message.content
    
    #开启多轮对话
    def start_chat_history(self, chat_id, prompt):
        self.chat_history[chat_id] = []
        self.chat_history[chat_id] = [
                    {"role": "system", "content": prompt}]
    
    #关闭多轮对话
    def stop_chat_history(self, chat_id):
        self.chat_history[chat_id] = []
    
    #多轮对话
    def get_response_with_history(self, chat_id, model, role, message):
        try:
            if not self.chat_history[chat_id] and role == "system":
                raise ValueError("未设置系统提示")
            
            self.chat_history[chat_id].append({"role": role, "content": message})               
                
            response = self.client.chat.completions.create(
            model = model,
            messages=self.chat_history[chat_id],
            stream=False
            )
            
            self.chat_history[chat_id].append({"role": "assistant", "content": response.choices[0].message.content})               
            return response.choices[0].message.content
        
        except Exception as e:
            logger.error(f"Error in get_response_with_history: {e}")