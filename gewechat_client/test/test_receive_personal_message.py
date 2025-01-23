import unittest
from unittest.mock import Mock, patch
from gewechat_client.receive_message.receive_personal_message import personal_message_handler

class TestPersonalMessageHandler(unittest.TestCase):
    @patch('gewechat_client.receive_message.receive_personal_message.PersonalMessageHandler')
    def test_personal_message_handler_MsgTypeIsOne(self, mock_handler):
        data = {
            "TypeName": "AddMsg",
            "Appid": "wx_wR_U4zPj2M_OTS3BCyoE4",
            "Wxid": "wxid_phyyedw9xap22",
            "Data": {
                "MsgId": 1040356095,
                "FromUserName": {"string": "wxid_phyyedw9xap22"},
                "ToUserName": {"string": "wxid_0xsqb3o0tsvz22"},
                "MsgType": 1,
                "Content": {"string": "123"},
                "Status": 3,
                "ImgStatus": 1,
                "ImgBuf": {"iLen": 0},
                "CreateTime": 1705043418,
                "MsgSource": "<msgsource>\n\t<alnode>\n\t\t<fr>1</fr>\n\t</alnode>\n\t<signature>v1_volHXhv4</signature>\n\t<tmp_node>\n\t\t<publisher-id></publisher-id>\n\t</tmp_node>\n</msgsource>\n",
                "PushContent": "朝夕。 : 123",
                "NewMsgId": 7773749793478223190,
                "MsgSeq": 640356095
            }
        }
        personal_message_handler(data)
        mock_handler.assert_called_once()
        mock_handler.return_value.handle_message.assert_called_once_with(data)
        
    # 测试群消息
    @patch('gewechat_client.receive_message.receive_personal_message.PersonalMessageHandler')
    def test_personal_message_handler_MsgTypeGroup(self, mock_handler):
        data = {
            "TypeName": "AddMsg",
            "Appid": "wx_wR_U4zPj2M_OTS3BCyoE4",
            "Wxid": "39292796878@chatroom",
            "Data": {
                "MsgId": 1040356095,
                "FromUserName": {"string": "wxid_phyyedw9xap22"},
                "ToUserName": {"string": "wxid_0xsqb3o0tsvz22"},
                "MsgType": 1,
                "Content": {"string": "123"},
                "Status": 3,
                "ImgStatus": 1,
                "ImgBuf": {"iLen": 0},
                "CreateTime": 1705043418,
                "MsgSource": "<msgsource>\n\t<alnode>\n\t\t<fr>1</fr>\n\t</alnode>\n\t<signature>v1_volHXhv4</signature>\n\t<tmp_node>\n\t\t<publisher-id></publisher-id>\n\t</tmp_node>\n</msgsource>\n",
                "PushContent": "朝夕。 : 123",
                "NewMsgId": 7773749793478223190,
                "MsgSeq": 640356095
            }
        }
        personal_message_handler(data)
    
    #测试handler_message
    def test_handler_message(self):
        data = {
            "TypeName": "AddMsg",
            "Appid": "wx_wR_U4zPj2M_OTS3BCyoE4",
            "Wxid": "39292796878@chatroom",
            "Data": {
                "MsgId": 1040356095,
                "FromUserName": {"string": "wxid_phyyedw9xap22"},
                "ToUserName": {"string": "wxid_0xsqb3o0tsvz22"},
                "MsgType": 1,
                "Content": {"string": "123"},
                "Status": 3,
                "ImgStatus": 1,
                "ImgBuf": {"iLen": 0},
                "CreateTime": 1705043418,
                "MsgSource": "<msgsource>\n\t<alnode>\n\t\t<fr>1</fr>\n\t</alnode>\n\t<signature>v1_volHXhv4</signature>\n\t<tmp_node>\n\t\t<publisher-id></publisher-id>\n\t</tmp_node>\n</msgsource>\n",
                "PushContent": "朝夕。 : 123",
                "NewMsgId": 7773749793478223190,
                "MsgSeq": 640356095
            }
        }
        handler = Mock()
        handler.handle_message(data)
