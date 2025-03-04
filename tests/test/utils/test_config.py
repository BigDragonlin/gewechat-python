import unittest
from unittest.mock import patch, mock_open
import os
import yaml
from src.gewechat.utils.config import load_config

class TestConfig(unittest.TestCase):
    
    @patch('builtins.open', new_callable=mock_open, read_data='''
log:
  level: INFO
  base_file: logs/gewechat.log
server:
  host: 127.0.0.1
  port: 8000
''')
    def test_load_config_default_path(self, mock_file):
        # 测试使用默认路径加载配置
        with patch.dict(os.environ, {}, clear=True):  # 清除环境变量
            config = load_config()
            
            # 验证配置内容
            self.assertEqual(config['log']['level'], 'INFO')
            self.assertEqual(config['log']['base_file'], 'logs/gewechat.log')
            self.assertEqual(config['server']['host'], '127.0.0.1')
            self.assertEqual(config['server']['port'], 8000)
            
            # 验证打开的文件路径
            mock_file.assert_called_once_with('gewechat_client/config.yaml', 'r')
    
    @patch('builtins.open', new_callable=mock_open, read_data='''
log:
  level: DEBUG
  base_file: logs/custom.log
''')
    def test_load_config_env_path(self, mock_file):
        # 测试使用环境变量指定的路径加载配置
        with patch.dict(os.environ, {'GEWECHAT_CONFIG_FILE': 'custom_config.yaml'}, clear=True):
            config = load_config()
            
            # 验证配置内容
            self.assertEqual(config['log']['level'], 'DEBUG')
            self.assertEqual(config['log']['base_file'], 'logs/custom.log')
            
            # 验证打开的文件路径
            mock_file.assert_called_once_with('custom_config.yaml', 'r')
    
    @patch('builtins.open', new_callable=mock_open, read_data='''
log:
  level: WARNING
  base_file: logs/specified.log
''')
    def test_load_config_specified_path(self, mock_file):
        # 测试使用指定路径加载配置
        config = load_config('specified_config.yaml')
        
        # 验证配置内容
        self.assertEqual(config['log']['level'], 'WARNING')
        self.assertEqual(config['log']['base_file'], 'logs/specified.log')
        
        # 验证打开的文件路径
        mock_file.assert_called_once_with('specified_config.yaml', 'r')
    
    @patch('builtins.open')
    def test_load_config_file_not_found(self, mock_file):
        # 测试文件不存在的情况
        mock_file.side_effect = FileNotFoundError()
        
        # 验证抛出异常
        with self.assertRaises(FileNotFoundError):
            load_config('nonexistent_config.yaml')

if __name__ == '__main__':
    unittest.main() 