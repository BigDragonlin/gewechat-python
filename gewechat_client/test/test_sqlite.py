import sqlite3
import unittest
from .. receive_message.receive_personal_message import *

import os
def create_table():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)''')
    conn.commit()
    conn.close()

def insert_user(name, age):
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (name, age) VALUES (?, ?)", (name, age))
    conn.commit()
    conn.close()

def get_users():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    conn.close()
    return users

class TestSQLite(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # 创建数据库和表
        # create_table()
        cls.personal_message_handler = message_handler()
        

    # @classmethod
    # def tearDownClass(cls):
    #     # 测试结束后删除数据库文件
    #     if os.path.exists('example.db'):
    #         os.remove('example.db')

    def test_insert_and_get_users(self):
        # 插入数据
        insert_user('Alice', 30)
        insert_user('Bob', 25)

        # 查询数据
        users = get_users()

        # 断言查询结果
        self.assertEqual(len(users), 2)
        self.assertEqual(users[0][1], 'Alice')
        self.assertEqual(users[0][2], 30)
        self.assertEqual(users[1][1], 'Bob')
        self.assertEqual(users[1][2], 25)
    
    # 将用户发送的消息放到sqlite中，私聊的话放到私聊数据库，群聊的话放到群聊数据库，群聊数据库里面有个字段是群聊id，私聊数据库里面有个字段是用户id
    # 测试插入私聊数据
    def test_insert_private_chat(self):
        message = {"name" : "bob", "message" : "hello world"}
        self.personal_message_handler.save_message(message)
        
    # 测试插入群聊数据
    def test_insert_group_chat(self):
        print("test_insert_group_chat")
    

if __name__ == '__main__':
    unittest.main()