import unittest
from unittest.mock import Mock, patch
from gewechat_client.receive_message.receive_personal_message import *
from gewechat_client.receive_message.callbackhandler import MessageHandler


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
        
        self.chatroom_data ={
            'TypeName': 'AddMsg',
            'Appid': 'wx_eK2IMGLgJyvVz7yPPN7ao',
            'Wxid': 'wxid_z60sn93h78so22',
            'Data': {
                'MsgId': 1395910907,
                'FromUserName': {
                    'string': '39292796878@chatroom'
                },
                'ToUserName': {
                    'string': 'wxid_z60sn93h78so22'
                },
                'MsgType': 1,
                'Content': {
                    'string': 'cml1363992060:\n测试'
                },
                'Status': 3,
                'ImgStatus': 1,
                'ImgBuf': {
                    'iLen': 0
                },
                'CreateTime': 1737708793,
                'MsgSource': '<msgsource>\n\t<sec_msg_node>\n\t\t<alnode>\n\t\t\t<fr>1</fr>\n\t\t</alnode>\n\t</sec_msg_node>\n\t<pua>1</pua>\n\t<silence>0</silence>\n\t<membercount>2</membercount>\n\t<signature>V1_kUaRcZe8|v1_kUaRcZe8</signature>\n\t<tmp_node>\n\t\t<publisher-id></publisher-id>\n\t</tmp_node>\n</msgsource>\n',
                'PushContent': '林木 : 测试',
                'NewMsgId': 3112724554915022913,
                'MsgSeq': 852986324
            }
        }
        
        self.chatroom_data_athelp ={
            'TypeName': 'AddMsg',
            'Appid': 'wx_eK2IMGLgJyvVz7yPPN7ao',
            'Wxid': 'wxid_z60sn93h78so22',
            'Data': {
                'MsgId': 1395910907,
                'FromUserName': {
                    'string': '39292796878@chatroom'
                },
                'ToUserName': {
                    'string': 'wxid_z60sn93h78so22'
                },
                'MsgType': 1,
                'Content': {
                    'string': 'cml1363992060:\n测试'
                },
                'Status': 3,
                'ImgStatus': 1,
                'ImgBuf': {
                    'iLen': 0
                },
                'CreateTime': 1737708793,
                'MsgSource': '<msgsource>\n\t<sec_msg_node>\n\t\t<alnode>\n\t\t\t<fr>1</fr>\n\t\t</alnode>\n\t</sec_msg_node>\n\t<pua>1</pua>\n\t<silence>0</silence>\n\t<membercount>2</membercount>\n\t<signature>V1_kUaRcZe8|v1_kUaRcZe8</signature>\n\t<tmp_node>\n\t\t<publisher-id></publisher-id>\n\t</tmp_node>\n</msgsource>\n',
                'PushContent': '林木 : @help',
                'NewMsgId': 3112724554915022913,
                'MsgSeq': 852986324
            }
        }
        
        self.chatroom_data_at_xingzuo ={
                'TypeName': 'AddMsg',
                'Appid': 'wx_z1C2XWFOi00Cb49yMxYp9',
                'Data': {
                    'MsgId': 580470092,
                    'FromUserName': {'string': '39292796878@chatroom'},
                    'ToUserName': {'string': 'wxid_z60sn93h78so22'},
                    'MsgType': 1,
                    'Content': {'string': 'cml1363992060:\n@机器人\u2005/星座 摩羯座'},
                    'Status': 3,
                    'ImgStatus': 1,
                    'ImgBuf': {'iLen': 0},
                    'CreateTime': 1740031769,
                    'MsgSource': '<msgsource>\n\t<alnode>\n\t\t<cf>2</cf>\n\t</alnode>\n\t<pua>1</pua>\n\t<silence>0</silence>\n\t<membercount>2</membercount>\n\t<signature>V1_gYkIex7Y|v1_gYkIex7Y</signature>\n\t<tmp_node>\n\t\t<publisher-id></publisher-id>\n\t</tmp_node>\n</msgsource>\n',
                    'PushContent': '林木 : @机器人\u2005/星座 摩羯座',
                    'NewMsgId': 974173506991559662,
                    'MsgSeq': 852987823},
                'Wxid': 'wxid_z60sn93h78so22'
                }
    def test_personal_message_handler(self):
        # 测试个人消息处理
        try:
            personal_data = self.personal_data
            MessageHandler().message_handler(personal_data)
        except Exception as e:
            print(f"Error occurred: {str(e)}")
    
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
        # personal_message_handler(data)
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
        # personal_message_handler(data)

    # 测试HandleMessage
    def test_handle_message_normal(self):
        # 测试正常消息处理
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
        self.message_handler.handle_message(data)

        # # 验证消息是否被正确保存到数据库
        # self.message_handler.cursor.execute("SELECT message FROM user_messages WHERE wx_id = ?", ("user123",))
        # result = self.message_handler.cursor.fetchone()
        # self.assertIsNotNone(result)
        # self.assertEqual(result[0], "Hello, World!")

    # 测试help
    def test_handle_message_help(self):
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
                "PushContent": "朝夕。 : @help",
                "NewMsgId": 7773749793478223190,
                "MsgSeq": 640356095
            }
        }
        self.message_handler.handle_message(data)

    # 测试打卡
    def test_handle_message_help(self):
        data = {
            "TypeName": "AddMsg",
            "Appid": "wx_wR_U4zPj2M_OTS3BCyoE4",
            "Wxid": "39292796878@chatroom",
            "Data": {
                "MsgId": 1040356095,
                "FromUserName": {"string": "39292796878@chatroom"},
                "ToUserName": {"string": "wxid_0xsqb3o0tsvz22"},
                "MsgType": 1,
                "Content": {"string": "123"},
                "Status": 3,
                "ImgStatus": 1,
                "ImgBuf": {"iLen": 0},
                "CreateTime": 1705043418,
                "MsgSource": "<msgsource>\n\t<alnode>\n\t\t<fr>1</fr>\n\t</alnode>\n\t<signature>v1_volHXhv4</signature>\n\t<tmp_node>\n\t\t<publisher-id></publisher-id>\n\t</tmp_node>\n</msgsource>\n",
                "PushContent": "朝夕。 : Day1石刻文献是以石头为物质载体的记录知识的文献形式，它的起源很早，《墨子》中就有“书于竹帛、镂于金石”的说法，说明金石和书籍是并行的。石刻文献作为文学的承载，主要集中于碑志和摩崖。其中一部分如碑版铭刻和摩崖石刻，流传久远；一部分如埋于墓中的墓志，多为后世出土，属于新出文献。",
                "NewMsgId": 7773749793478223190,
                "MsgSeq": 640356095
            }
        }
        self.message_handler.handle_message(data)

    # 测试打卡
    def test_handle_message_group(self):
        data = {
            'TypeName': 'AddMsg',
            'Appid': 'wx_eK2IMGLgJyvVz7yPPN7ao',
            'Wxid': 'wxid_z60sn93h78so22',
            'Data': {
                'MsgId': 1395910907,
                'FromUserName': {
                    'string': '39292796878@chatroom'
                },
                'ToUserName': {
                    'string': 'wxid_z60sn93h78so22'
                },
                'MsgType': 1,
                'Content': {
                    'string': 'cml1363992060:\n测试'
                },
                'Status': 3,
                'ImgStatus': 1,
                'ImgBuf': {
                    'iLen': 0
                },
                'CreateTime': 1737708793,
                'MsgSource': '<msgsource>\n\t<sec_msg_node>\n\t\t<alnode>\n\t\t\t<fr>1</fr>\n\t\t</alnode>\n\t</sec_msg_node>\n\t<pua>1</pua>\n\t<silence>0</silence>\n\t<membercount>2</membercount>\n\t<signature>V1_kUaRcZe8|v1_kUaRcZe8</signature>\n\t<tmp_node>\n\t\t<publisher-id></publisher-id>\n\t</tmp_node>\n</msgsource>\n',
                'PushContent': '林木 : 测试',
                'NewMsgId': 3112724554915022913,
                'MsgSeq': 852986324
            }
        }
        self.message_handler.handle_message(data)
    # 测试打卡
    
    def test_handle_message_group_checkin(self):
        data = {
            'TypeName': 'AddMsg',
            'Appid': 'wx_eK2IMGLgJyvVz7yPPN7ao',
            'Wxid': 'wxid_z60sn93h78so22',
            'Data': {
                'MsgId': 1395910907,
                'FromUserName': {
                    'string': '39292796878@chatroom'
                },
                'ToUserName': {
                    'string': 'wxid_z60sn93h78so22'
                },
                'MsgType': 1,
                'Content': {
                    'string': 'cml1363992060:\n测试'
                },
                'Status': 3,
                'ImgStatus': 1,
                'ImgBuf': {
                    'iLen': 0
                },
                'CreateTime': 1737708793,
                'MsgSource': '<msgsource>\n\t<sec_msg_node>\n\t\t<alnode>\n\t\t\t<fr>1</fr>\n\t\t</alnode>\n\t</sec_msg_node>\n\t<pua>1</pua>\n\t<silence>0</silence>\n\t<membercount>2</membercount>\n\t<signature>V1_kUaRcZe8|v1_kUaRcZe8</signature>\n\t<tmp_node>\n\t\t<publisher-id></publisher-id>\n\t</tmp_node>\n</msgsource>\n',
                "PushContent": "朝夕。 : Day1石刻文献是以石头为物质载体的记录知识的文献形式，它的起源很早，《墨子》中就有“书于竹帛、镂于金石”的说法，说明金石和书籍是并行的。石刻文献作为文学的承载，主要集中于碑志和摩崖。其中一部分如碑版铭刻和摩崖石刻，流传久远；一部分如埋于墓中的墓志，多为后世出土，属于新出文献。",
                'NewMsgId': 3112724554915022913,
                'MsgSeq': 852986324
            }
        }
        self.message_handler.handle_message(data)
