import unittest
from unittest.mock import Mock, patch
from gewechat_client.receive_message.receive_group_message import *
from gewechat_client.receive_message.callbackhandler import MessageHandler

class TestGroupMessageHandler(unittest.TestCase):
    def setUp(self):
        self.group_message_handler = GroupMessageHandler()
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
    
    def test_group_message_handler(self):
        """测试群消息处理"""
        try:
            group_data = self.chatroom_data
            MessageHandler().message_handler(group_data)
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            
    def test_group_message_athelp(self):
        """测试群at help消息处理"""   
        try:
            group_data = self.chatroom_data_athelp
            MessageHandler().message_handler(group_data)
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            
    def test_group_message_at_xingzuo(self):
        """测试群at星座 消息处理"""
        try:
            group_data = self.chatroom_data_at_xingzuo
            MessageHandler().message_handler(group_data)
        except Exception as e:
            print(f"Error occurred: {str(e)}")
    
    
    def test_group_process_group_at_message(self):
        """测试群at消息处理"""
        message = "@机器人\u2005/星座 摩羯座"
        response = self.group_message_handler.process_group_at_message(message, None)
        print(response)