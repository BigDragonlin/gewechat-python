import unittest
import sqlite3
from gewechat_client.util.db import SqliteDB

class TestSQLite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 创建数据库和表
        # create_table()
        cls.sqliteDB = SqliteDB()
        

    # @classmethod
    # def tearDownClass(cls):
    #     # 测试结束后删除数据库文件
    #     if os.path.exists('example.db'):
    #         os.remove('example.db')
    
    def test_save_message(self):
        # 测试保存消息
        self.sqliteDB.save_message('test_sender', 'test_message')
        
        # 查询数据库并验证结果
        cursor = self.sqliteDB.conn.cursor()
        cursor.execute("SELECT * FROM user_messages WHERE wx_id='test_sender'")
        result = cursor.fetchone()
        self.assertIsNotNone(result)
    
    def test_save_answer(self):
        # 测试保存答案
        self.sqliteDB.save_answer('test_wx_id', 'test_answer')
        messages = self.sqliteDB.select_answer()
        print(messages[0][0])
        self.assertIsNotNone(messages)
        self.sqliteDB.delete_answer(messages[0][0])
    

if __name__ == '__main__':
    unittest.main()