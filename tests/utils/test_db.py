import unittest
import sqlite3
from unittest.mock import patch, MagicMock
import os
import tempfile
from src.gewechat.utils.db import SqliteDB

class TestSqliteDB(unittest.TestCase):
    
    def setUp(self):
        # 创建临时数据库文件
        self.temp_db_fd, self.temp_db_path = tempfile.mkstemp()
        # 修改SqliteDB的db_path属性，使用临时文件
        self.patcher = patch.object(SqliteDB, 'db_path', self.temp_db_path)
        self.patcher.start()
        # 重置单例
        SqliteDB._instance = None
        SqliteDB._initialized = False
        # 创建数据库实例
        self.db = SqliteDB()
    
    def tearDown(self):
        # 停止patch
        self.patcher.stop()
        # 关闭并删除临时文件
        os.close(self.temp_db_fd)
        os.unlink(self.temp_db_path)
    
    def test_singleton_pattern(self):
        # 测试单例模式
        db1 = SqliteDB()
        db2 = SqliteDB()
        self.assertIs(db1, db2)
    
    def test_initialize_tables(self):
        # 测试表初始化
        conn = sqlite3.connect(self.temp_db_path)
        cursor = conn.cursor()
        
        # 检查messages表是否存在
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='messages'")
        self.assertIsNotNone(cursor.fetchone())
        
        # 检查answers表是否存在
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='answers'")
        self.assertIsNotNone(cursor.fetchone())
        
        conn.close()
    
    def test_save_and_select_message(self):
        # 测试保存消息
        sender_wx_id = "test_user"
        message = "测试消息"
        self.db.save_message(sender_wx_id, message)
        
        # 直接查询数据库验证
        conn = sqlite3.connect(self.temp_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT sender_wx_id, message FROM messages WHERE sender_wx_id=?", (sender_wx_id,))
        result = cursor.fetchone()
        conn.close()
        
        self.assertIsNotNone(result)
        self.assertEqual(result[0], sender_wx_id)
        self.assertEqual(result[1], message)
    
    def test_save_and_select_answer(self):
        # 测试保存和查询回答
        wx_id = "test_user"
        message = "测试回答"
        self.db.save_answer(wx_id, message)
        
        # 查询回答
        answers = self.db.select_answer()
        
        self.assertTrue(len(answers) > 0)
        found = False
        for answer in answers:
            if answer[1] == wx_id and answer[2] == message:
                found = True
                break
        self.assertTrue(found)
    
    def test_delete_answer(self):
        # 测试删除回答
        wx_id = "test_user_delete"
        message = "测试删除回答"
        self.db.save_answer(wx_id, message)
        
        # 查询回答获取ID
        answers = self.db.select_answer()
        answer_id = None
        for answer in answers:
            if answer[1] == wx_id and answer[2] == message:
                answer_id = answer[0]
                break
        
        self.assertIsNotNone(answer_id)
        
        # 删除回答
        self.db.delete_answer(answer_id)
        
        # 再次查询确认已删除
        answers_after_delete = self.db.select_answer()
        found = False
        for answer in answers_after_delete:
            if answer[0] == answer_id:
                found = True
                break
        self.assertFalse(found)
    
    def test_thread_safety(self):
        # 测试线程安全性
        # 这里只是简单测试，实际上需要更复杂的多线程测试
        db1 = SqliteDB()
        db2 = SqliteDB()
        
        # 两个实例应该是同一个对象
        self.assertIs(db1, db2)
        
        # 但它们应该有独立的thread_local
        self.assertIsNot(db1.thread_local, db2.thread_local)

if __name__ == '__main__':
    unittest.main() 