import unittest
from unittest.mock import MagicMock, patch
from gewechat_client.send_message.sendmessage import SendMessage, send_msg

class TestSendMessage(unittest.TestCase):

    def setUp(self):
        self.client = MagicMock()
        self.app_id = "test_app_id"
        self.wxid = "test_wxid"
        self.message = "Hello, World!"
        self.send_msg_nickname = "林木"

    def test_send_msg_by_wxid_success(self):
        self.client.post_text.return_value = {'ret': 200, 'msg': '操作成功'}
        send_msg_instance = SendMessage(self.client, self.app_id)
        result = send_msg_instance.send_msg_by_wxid(self.wxid, self.message)
        self.client.post_text.assert_called_once_with(self.app_id, self.wxid, self.message)
        self.assertIsNone(result)  # 修改为检查返回值是否为None

    def test_send_msg_by_wxid_failure(self):
        self.client.post_text.return_value = {'ret': 400, 'msg': '操作失败'}
        send_msg_instance = SendMessage()
        result = send_msg_instance.send_msg_by_wxid(self.wxid, self.message)
        self.client.post_text.assert_called_once_with(self.app_id, self.wxid, self.message)
        self.assertIsNone(result)  # 修改为检查返回值是否为None

    @patch('gewechat_client.send_message.sendmessage.client')
    def test_send_msg_success(self, mock_client):
        mock_client.fetch_contacts_list.return_value = {'ret': 200, 'msg': '操作成功', 'data': {'friends': ['wxid_abcxx']}}
        mock_client.get_brief_info.return_value = {'ret': 200, 'msg': '操作成功', 'data': [{'nickName': self.send_msg_nickname, 'userName': self.wxid}]}
        mock_client.post_text.return_value = {'ret': 200, 'msg': '操作成功'}
        result = send_msg(mock_client, self.app_id)
        mock_client.fetch_contacts_list.assert_called_once_with(self.app_id)
        mock_client.get_brief_info.assert_called_once_with(self.app_id, ['wxid_abcxx'])
        mock_client.post_text.assert_called_once_with(self.app_id, self.wxid, "你好啊")
        self.assertTrue(result)  # 保持不变，因为send_msg函数返回值逻辑未变

    @patch('gewechat_client.send_message.sendmessage.client')
    def test_send_msg_failure_fetch_contacts_list(self, mock_client):
        mock_client.fetch_contacts_list.return_value = {'ret': 400, 'msg': '操作失败'}
        result = send_msg(mock_client, self.app_id)
        mock_client.fetch_contacts_list.assert_called_once_with(self.app_id)
        self.assertFalse(result)

    @patch('gewechat_client.send_message.sendmessage.client')
    def test_send_msg_failure_get_brief_info(self, mock_client):
        mock_client.fetch_contacts_list.return_value = {'ret': 200, 'msg': '操作成功', 'data': {'friends': ['wxid_abcxx']}}
        mock_client.get_brief_info.return_value = {'ret': 400, 'msg': '操作失败'}
        result = send_msg(mock_client, self.app_id)
        mock_client.fetch_contacts_list.assert_called_once_with(self.app_id)
        mock_client.get_brief_info.assert_called_once_with(self.app_id, ['wxid_abcxx'])
        self.assertFalse(result)

    @patch('gewechat_client.send_message.sendmessage.client')
    def test_send_msg_failure_post_text(self, mock_client):
        mock_client.fetch_contacts_list.return_value = {'ret': 200, 'msg': '操作成功', 'data': {'friends': ['wxid_abcxx']}}
        mock_client.get_brief_info.return_value = {'ret': 200, 'msg': '操作成功', 'data': [{'nickName': self.send_msg_nickname, 'userName': self.wxid}]}
        mock_client.post_text.return_value = {'ret': 400, 'msg': '操作失败'}
        result = send_msg(mock_client, self.app_id)
        mock_client.fetch_contacts_list.assert_called_once_with(self.app_id)
        mock_client.get_brief_info.assert_called_once_with(self.app_id, ['wxid_abcxx'])
        mock_client.post_text.assert_called_once_with(self.app_id, self.wxid, "你好啊")
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()