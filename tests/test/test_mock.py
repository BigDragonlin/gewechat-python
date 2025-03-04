import unittest
from unittest.mock import Mock, call

# 真实类定义保持不变
class RealHttpClient:
    def __init__(self, host):
        self.host = host
        
    def connect(self):
        return True
    
    def send_request(self, method, path):
        return f"{method} {self.host}{path}"
    
    def close(self):
        pass

class TestRealHttpClientMock(unittest.TestCase):
    def setUp(self):
        """初始化Mock对象"""
        self.mock_client = Mock(
            spec=RealHttpClient,                 # 指定模拟类，自动继承其所有方法签名（自动补全校验）
            spec_set=['connect', 'send_request', 'disconnect'],  # 严格限制可访问属性（白名单约束）
            disconnect=Mock(return_value=True),  # 为disconnect方法配置固定返回值
            wraps=RealHttpClient("https://api.example.com"),  # 包装真实对象实现，代理方法调用
            name="HttpClientMock",               # 设置mock对象名称（调试显示用） 
            version="1.0"                        # 添加额外属性（动态扩展测试属性）
        )
        # 单独配置connect方法的side_effect
        # 配置connect方法的side_effect（副作用链式响应）
        # side_effect 实现动态响应机制，允许：
        # 1. 按调用顺序返回不同值
        # 2. 抛出指定异常
        # 3. 返回复杂数据结构
        # 此配置用于测试connect方法在不同场景下的行为：
        # - 首次调用成功返回布尔值
        # - 第二次模拟网络超时异常
        # - 第三次返回非常规响应数据（测试异常数据处理）
        self.mock_client.connect.side_effect = [
            # 第一个调用返回True（模拟成功连接）
            lambda: True,               
            # 第二个调用抛出TimeoutError（模拟网络超时场景）
            TimeoutError(),             
            # 第三个调用返回字典（测试非标准返回值的处理能力）
            {'status': 200}             
            # 注意：列表元素的顺序必须与测试用例中的调用顺序严格一致
            # 每个元素可以是：
            # - 可调用对象（自动执行）
            # - 异常实例（触发抛出）
            # - 任意值（直接返回）
        ]
        
    def test_spec_constraint(self):
        """验证spec属性约束"""
        with self.assertRaises(AttributeError) as context:
            self.mock_client.nonexistent_method()
        self.assertIn("has no attribute 'nonexistent_method'", str(context.exception))

    def test_connect_behavior(self):
        """验证connect方法的三次调用行为"""
        # 第一次调用返回True
        self.assertTrue(self.mock_client.connect())
        # 第二次调用抛出TimeoutError
        with self.assertRaises(TimeoutError):
            self.mock_client.connect()
        # 第三次调用返回字典
        self.assertEqual(self.mock_client.connect(), {'status': 200})
        # 验证调用次数和顺序
        self.mock_client.connect.assert_has_calls([call(), call(), call()])

    def test_wrapped_implementation(self):
        """验证包装的真实对象方法"""
        result = self.mock_client.send_request("GET", "/data")
        self.assertEqual(result, "GET https://api.example.com/data")

    def test_disconnect_behavior(self):
        """验证disconnect固定返回值"""
        self.assertTrue(self.mock_client.disconnect())

    def test_extra_attribute(self):
        """验证额外属性"""
        self.assertEqual(self.mock_client.version, "1.0")

    def test_spec_set_constraint(self):
        """验证spec_set属性约束"""
        with self.assertRaises(AttributeError) as context:
            self.mock_client.new_property = "test"
        self.assertIn("has no attribute 'new_property'", str(context.exception))

if __name__ == "__main__":
    unittest.main()