import unittest
from unittest.mock import Mock, patch
from src.gewechat.message.receive_message.receive_personal_message import *
from src.gewechat.message.receive_message.callbackhandler import message_handler


class TestPersonalMessageHandler(unittest.TestCase):
    def setUp(self):
        self.personal_data = {
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
                "PushContent": "朝夕。 :\n 123",
                "NewMsgId": 7773749793478223190,
                "MsgSeq": 640356095
            }
        }
        
    def test_personal_message_handler(self):
        # 测试个人消息处理
        try:
            personal_data = self.personal_data
            message_handler(personal_data)
        except Exception as e:
            print(f"Error occurred: {str(e)}")