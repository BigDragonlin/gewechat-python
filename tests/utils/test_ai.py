import unittest
from unittest.mock import patch, MagicMock
from src.gewechat.utils.ai import Ai

class TestAi(unittest.TestCase):
    
    @patch('src.gewechat.utils.ai.OpenAI')
    def setUp(self, mock_openai):
        # 设置模拟OpenAI客户端
        self.mock_client = MagicMock()
        mock_openai.return_value = self.mock_client
        
        # 创建Ai实例
        self.ai = Ai()
    
    def test_singleton_pattern(self):
        # 测试单例模式
        ai1 = Ai()
        ai2 = Ai()
        self.assertIs(ai1, ai2)
    
    def test_get_response(self):
        # 设置模拟响应
        mock_response = MagicMock()
        mock_message = MagicMock()
        mock_message.content = "这是一个测试回答"
        mock_choice = MagicMock()
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]
        self.mock_client.chat.completions.create.return_value = mock_response
        
        # 调用被测试的方法
        model = "gpt-3.5-turbo"
        user_message = "你好"
        system_prompt = "你是一个助手"
        
        result = self.ai.get_response(model, user_message, system_prompt)
        
        # 验证请求参数
        self.mock_client.chat.completions.create.assert_called_once_with(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            stream=False
        )
        
        # 验证结果
        self.assertEqual(result, "这是一个测试回答")
    
    def test_start_chat_history(self):
        # 测试开始聊天历史
        chat_id = "test_chat_id"
        prompt = "测试系统提示"
        
        self.ai.start_chat_history(chat_id, prompt)
        
        # 验证聊天历史是否正确初始化
        self.assertIn(chat_id, self.ai.chat_history)
        self.assertEqual(self.ai.chat_history[chat_id], [{"role": "system", "content": prompt}])
    
    def test_stop_chat_history(self):
        # 测试停止聊天历史
        chat_id = "test_chat_id"
        prompt = "测试系统提示"
        
        # 先创建聊天历史
        self.ai.start_chat_history(chat_id, prompt)
        self.assertIn(chat_id, self.ai.chat_history)
        
        # 停止聊天历史
        self.ai.stop_chat_history(chat_id)
        
        # 验证聊天历史是否被删除
        self.assertNotIn(chat_id, self.ai.chat_history)
    
    def test_get_response_with_history(self):
        # 设置模拟响应
        mock_response = MagicMock()
        mock_message = MagicMock()
        mock_message.content = "这是一个带历史的测试回答"
        mock_choice = MagicMock()
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]
        self.mock_client.chat.completions.create.return_value = mock_response
        
        # 准备测试数据
        chat_id = "test_chat_id"
        model = "gpt-3.5-turbo"
        prompt = "你是一个助手"
        
        # 开始聊天历史
        self.ai.start_chat_history(chat_id, prompt)
        
        # 调用被测试的方法
        result = self.ai.get_response_with_history(chat_id, model, "user", "你好")
        
        # 验证聊天历史是否更新
        self.assertEqual(len(self.ai.chat_history[chat_id]), 3)  # system + user + assistant
        self.assertEqual(self.ai.chat_history[chat_id][1], {"role": "user", "content": "你好"})
        self.assertEqual(self.ai.chat_history[chat_id][2], {"role": "assistant", "content": "这是一个带历史的测试回答"})
        
        # 验证结果
        self.assertEqual(result, "这是一个带历史的测试回答")

if __name__ == '__main__':
    unittest.main() 