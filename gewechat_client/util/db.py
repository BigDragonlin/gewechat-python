import sqlite3
from ..util.log import logger

class SqliteDB:
    _instance = None
    def __new__(cls):
        if cls._instance == None:
            cls._instance = object.__new__(cls)
            cls._instance._initialized = False
            return cls._instance
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
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
    
    def save_message(self, sender_wx_id, message):
        """保存消息到数据库"""
        try:
            self.cursor.execute("INSERT INTO user_messages (wx_id, message) VALUES (?, ?)", (sender_wx_id, message))
            self.conn.commit()
        except Exception as e:
            logger.exception(f"保存消息到数据库失败{str(e)}")
            self.conn.rollback()
     
    def save_answer(self, wx_id, message):
        """保存回答到数据库"""
        try:
            self.cursor.execute("INSERT INTO answer_queue_personal (wx_id, message) VALUES (?, ?)", (wx_id, message))
            self.conn.commit()
        except Exception as e:
            logger.exception(f"保存回答到数据库失败{str(e)}")
            self.conn.rollback
    
    def select_answer(self):
        """查询回答数据库中的消息"""
        try:
             messages = self.cursor.execute('SELECT * FROM answer_queue_personal').fetchall()
             self.conn.commit()
             return messages
        except Exception as e:
            logger.exception(f"查询回答数据库中的消息失败{str(e)}")
    
    def delete_answer(self, id):
        """删除回答数据库中的消息"""
        try:
            self.cursor.execute("DELETE FROM answer_queue_personal WHERE id = ?", (id,))
            self.conn.commit()
            return True
        except Exception as e:
            logger.exception(f"删除回答数据库中的消息失败{str(e)}")
            return False