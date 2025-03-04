import unittest
from gewechat_client.util.log import logger

class Test_logger(unittest.TestCase):
    def test_logger(self):
        logger.info("测试日志系统")
