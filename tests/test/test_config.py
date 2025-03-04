import unittest
from gewechat_client.util.config import load_config

class Test_Config(unittest.TestCase):
    
    def test_load_config(self):
        config = load_config()