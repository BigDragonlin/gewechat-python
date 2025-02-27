import unittest
from unittest.mock import Mock, patch
from gewechat_client.receive_message.receive_group_message import *
from gewechat_client.receive_message.callbackhandler import message_handler

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
        self.chatroom_data_xingzuo1 = {
            'TypeName': 'AddMsg',
            'Appid': 'wx_y3YVd3uP0QI0BAJKnjJr4', 'Data': {
                'MsgId': 1241327488,
                'FromUserName':     {'string':'53264107763@chatroom'},
                'ToUserName': 
                {'string': 'wxid_z60sn93h78so22'}, 'MsgType': 1,
                'Content': 
                    {'string': 'cml1363992060:\n@机器人\u2005/星座 金牛座'}, 
                'Status': 3,
                'ImgStatus': 1,
                'ImgBuf': {'iLen': 0},
                'CreateTime': 1740552652, 'MsgSource': '<msgsource>\n\t<alnode>\n\t\t<cf>2</cf>\n\t</alnode>\n\t<pua>1</pua>\n\t<silence>1</silence>\n\t<membercount>6</membercount>\n\t<signature>V1_xaZW8jOU|v1_xaZW8jOU</signature>\n\t<tmp_node>\n\t\t<publisher-id></publisher-id>\n\t</tmp_node>\n</msgsource>\n', 'NewMsgId': 6973432079026434027, 'MsgSeq': 852988438},
            'Wxid': 'wxid_z60sn93h78so22'
            }
    
    
        self.chatroom_data_start_ai ={
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
                    'PushContent': '林木 : /开启 AI',
                    'NewMsgId': 974173506991559662,
                    'MsgSeq': 852987823},
                'Wxid': 'wxid_z60sn93h78so22'
                }
    
        self.chatroom_data_stop_ai ={
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
                    'PushContent': '林木 : /关闭',
                    'NewMsgId': 974173506991559662,
                    'MsgSeq': 852987823},
                'Wxid': 'wxid_z60sn93h78so22'
                }

        self.chatroom_data_yunqi={
                'TypeName': 'AddMsg',
                'Appid': 'wx_z1C2XWFOi00Cb49yMxYp9',
                'Data': {
                    'MsgId': 580470092,
                    'FromUserName': {'string': '39292796878@chatroom'},
                    'ToUserName': {'string': 'wxid_z60sn93h78so22'},
                    'MsgType': 1,
                    'Content': {'string': 'cml1363992060:\n@机器人\u2005/运气 摩羯座'},
                    'Status': 3,
                    'ImgStatus': 1,
                    'ImgBuf': {'iLen': 0},
                    'CreateTime': 1740031769,
                    'MsgSource': '<msgsource>\n\t<alnode>\n\t\t<cf>2</cf>\n\t</alnode>\n\t<pua>1</pua>\n\t<silence>0</silence>\n\t<membercount>2</membercount>\n\t<signature>V1_gYkIex7Y|v1_gYkIex7Y</signature>\n\t<tmp_node>\n\t\t<publisher-id></publisher-id>\n\t</tmp_node>\n</msgsource>\n',
                    'PushContent': '林木 : /关闭',
                    'NewMsgId': 974173506991559662,
                    'MsgSeq': 852987823},
                'Wxid': 'wxid_z60sn93h78so22'
                }
        self.chatroom_data_lingqian={
                'TypeName': 'AddMsg',
                'Appid': 'wx_z1C2XWFOi00Cb49yMxYp9',
                'Data': {
                    'MsgId': 580470092,
                    'FromUserName': {'string': '39292796878@chatroom'},
                    'ToUserName': {'string': 'wxid_z60sn93h78so22'},
                    'MsgType': 1,
                    'Content': {'string': 'cml1363992060:\n@机器人\u2005/灵签 观音'},
                    'Status': 3,
                    'ImgStatus': 1,
                    'ImgBuf': {'iLen': 0},
                    'CreateTime': 1740031769,
                    'MsgSource': '<msgsource>\n\t<alnode>\n\t\t<cf>2</cf>\n\t</alnode>\n\t<pua>1</pua>\n\t<silence>0</silence>\n\t<membercount>2</membercount>\n\t<signature>V1_gYkIex7Y|v1_gYkIex7Y</signature>\n\t<tmp_node>\n\t\t<publisher-id></publisher-id>\n\t</tmp_node>\n</msgsource>\n',
                    'PushContent': '林木 : /关闭',
                    'NewMsgId': 974173506991559662,
                    'MsgSeq': 852987823},
                'Wxid': 'wxid_z60sn93h78so22'
                }

    def test_group_message_handler(self):
        """测试群消息处理"""
        try:
            group_data = self.chatroom_data
            message_handler(group_data)
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            
    def test_group_message_athelp(self):
        """测试群at help消息处理"""   
        try:
            group_data = self.chatroom_data_athelp
            message_handler(group_data)
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            
    def test_group_message_at_xingzuo(self):
        """测试群at星座 消息处理"""
        try:
            group_data = self.chatroom_data_at_xingzuo
            message_handler(group_data)
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            
    def test_group_message_at_xingzuo1(self):
        """测试群at星座 消息处理"""
        try:
            group_data = self.chatroom_data_xingzuo1
            message_handler(group_data)
        except Exception as e:
            print(f"Error occurred: {str(e)}")
    #测试运气
    def test_group_process_message_yunqi(self):
        """测试群消息处理"""
        message = self.chatroom_data_yunqi
        response = message_handler(message)
        print(response)
    
    #测试灵签
    def test_group_process_message_lingqian(self):
        """测试群消息处理"""
        message = self.chatroom_data_lingqian
        response = message_handler(message)
        print(response)
    
    def test_group_process_group_at_message(self):
        """测试群at消息处理"""
        message = "@机器人\u2005/星座 摩羯座"
        response = message_handler(self.chatroom_data_at_xingzuo)
        print(response)
    
    #测试ai开启
    def test_group_process_message_atart_ai(self):
        """测试群消息处理"""
        message = self.chatroom_data_start_ai
        response = message_handler(message)
        print(response)
    
    #测试ai关闭
    def test_group_process_message_atstop_ai(self):
        """测试群消息处理"""
        message = self.chatroom_data_stop_ai
        response = message_handler(message)
        print(response)
    
    #测试ai对话
    def test_group_process_message_ai(self):
        """测试群消息处理"""
        self.group_message_handler.process_message("/开启 AI", "wxid_z60sn93h78so22", self.chatroom_data)
        self.group_message_handler.process_message("你好", "wxid_z60sn93h78so22", self.chatroom_data)

    