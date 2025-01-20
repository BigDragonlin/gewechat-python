import unittest
from unittest.mock import MagicMock, patch
from gewechat_client.send_message.sendmessage import SendMessage, send_msg

class TestSendMessage(unittest.TestCase):
    def setUp(self):
        self.send_message = SendMessage(MagicMock(), MagicMock())
        self.send_message.init_database_personal_queue("../../messages.db","answer_queue_personal")
    #测试查询
    def test_select_database_personal_by_wx_id(self):
        self.send_message.insert_database_personal_queue("11", "测试回答1")
        self.send_message.insert_database_personal_queue("22", "测试回答2")
        result = self.send_message.select_database_personal_by_wx_id()
        print(result)
        
if __name__ == '__main__':
    unittest.main()