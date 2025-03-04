import unittest
from unittest.mock import MagicMock, patch
from src.gewechat.message.send_message.sendmessage import SendMessage, run_send_message_server
from src.gewechat.api.client import GewechatClient

import src.gewechat.message.send_message.sendmessage as target_module

class TestSendMessage(unittest.TestCase):
    def setUp(self):
        pass
    def test_send_msg_by_wxid(self):
        self.send_message.send_msg_by_wxid("test_wxid", "test_message")

    
    @patch(f"{target_module.__name__}.SqliteDB")
    @patch(f"{target_module.__name__}.SendMessage")
    def test_send_msg_server(self, mock_send_message, mock_sqlite_db):
        # 设置SendMessage的模拟行为
        mock_send_handler = mock_send_message.return_value
        mock_send_handler.friends_id = ["test_wxid"]
        mock_send_handler.send_msg_by_wxid = MagicMock()

        # 设施SqliteDB的模拟行为
        mock_db_instance = mock_sqlite_db.return_value
        mock_db_instance.select_answer.return_value = [("1","test_wxid", "test_message", "2021-01-01")]
        mock_db_instance.delete_answer = MagicMock()
        #创建模拟的
        client = MagicMock(spec=GewechatClient)
        run_send_message_server(client, "test_app_id")
               
        # mock_send_handler.send_msg_by_wxid.assert_called_once_with("test_wxid", "test_message")
        # mock_db_instance.delete_answer.assert_called_once_with(1)
        

if __name__ == '__main__':
    unittest.main()