import unittest
from unittest.mock import patch, MagicMock
import logging
from src.gewechat.utils.log import logger

class TestLogger(unittest.TestCase):
    
    @patch('logging.Logger.info')
    def test_logger_info(self, mock_info):
        # 测试info级别日志
        test_message = "测试信息日志"
        logger.info(test_message)
        mock_info.assert_called_once_with(test_message)
    
    @patch('logging.Logger.warning')
    def test_logger_warning(self, mock_warning):
        # 测试warning级别日志
        test_message = "测试警告日志"
        logger.warning(test_message)
        mock_warning.assert_called_once_with(test_message)
    
    @patch('logging.Logger.error')
    def test_logger_error(self, mock_error):
        # 测试error级别日志
        test_message = "测试错误日志"
        logger.error(test_message)
        mock_error.assert_called_once_with(test_message)
    
    @patch('logging.Logger.debug')
    def test_logger_debug(self, mock_debug):
        # 测试debug级别日志
        test_message = "测试调试日志"
        logger.debug(test_message)
        mock_debug.assert_called_once_with(test_message)
    
    @patch('logging.Logger.critical')
    def test_logger_critical(self, mock_critical):
        # 测试critical级别日志
        test_message = "测试严重错误日志"
        logger.critical(test_message)
        mock_critical.assert_called_once_with(test_message)
    
    def test_logger_name(self):
        # 测试logger名称
        self.assertEqual(logger.name, "src.gewechat.utils.log")

if __name__ == '__main__':
    unittest.main() 