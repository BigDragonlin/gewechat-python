import unittest
from src.gewechat.utils.log import logger

class Test_logger(unittest.TestCase):
    def test_logger(self):
        logger.info("测试日志系统")
