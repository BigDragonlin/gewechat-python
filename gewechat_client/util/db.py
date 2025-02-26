import sqlite3
import threading
from ..util.log import logger

class SqliteDB:
    _instance = None
    _lock = threading.Lock()  # 用于单例初始化的线程安全

    def __new__(cls):
        with cls._lock:  # 确保单例创建线程安全
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self):
        if not self._initialized:
            self.db_path = 'messages.db'
            self.thread_local = threading.local()  # 每个线程独立的存储
            self._initialized = True
            # 初始化数据库表只在首次创建时执行
            self._initialize_tables()

    def _get_conn(self):
        """为当前线程获取或创建数据库连接"""
        if not hasattr(self.thread_local, 'conn'):
            self.thread_local.conn = sqlite3.connect(self.db_path)
            self.thread_local.cursor = self.thread_local.conn.cursor()
        return self.thread_local.conn, self.thread_local.cursor

    def _initialize_tables(self):
        """初始化数据库表"""
        conn, cursor = self._get_conn()
        try:
            # 初始化个人聊天信息库
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    wx_id TEXT NOT NULL,
                    message TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            # 初始化回答队列数据库
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS answer_queue_personal (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    wx_id TEXT NOT NULL,
                    message TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            # 初始化打卡数据库
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS checkin_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    wx_id TEXT NOT NULL,
                    message TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
        except Exception as e:
            logger.exception(f"初始化数据库表失败: {str(e)}")
            conn.rollback()

    def save_message(self, sender_wx_id, message):
        """保存消息到数据库"""
        conn, cursor = self._get_conn()
        try:
            cursor.execute("INSERT INTO user_messages (wx_id, message) VALUES (?, ?)", (sender_wx_id, message))
            conn.commit()
        except Exception as e:
            logger.exception(f"保存消息到数据库失败: {str(e)}")
            conn.rollback()

    def save_answer(self, wx_id, message):
        """保存回答到数据库"""
        conn, cursor = self._get_conn()
        try:
            cursor.execute("INSERT INTO answer_queue_personal (wx_id, message) VALUES (?, ?)", (wx_id, message))
            conn.commit()
        except Exception as e:
            logger.exception(f"保存回答到数据库失败: {str(e)}")
            conn.rollback()

    def select_answer(self):
        """查询回答数据库中的消息"""
        conn, cursor = self._get_conn()
        try:
            cursor.execute("SELECT * FROM answer_queue_personal")
            messages = cursor.fetchall()
            # 无需手动 commit，因为 SELECT 不修改数据
            return messages
        except Exception as e:
            logger.exception(f"查询回答数据库中的消息失败: {str(e)}")
            return []

    def delete_answer(self, id):
        """删除回答数据库中的消息"""
        conn, cursor = self._get_conn()
        try:
            cursor.execute("DELETE FROM answer_queue_personal WHERE id = ?", (id,))
            conn.commit()
            return True
        except Exception as e:
            logger.exception(f"删除回答数据库中的消息失败: {str(e)}")
            conn.rollback()
            return False