import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
from src.gewechat.utils.terminal_printer import print_green, print_yellow, print_red, make_and_print_qr

class TestTerminalPrinter(unittest.TestCase):
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_print_green(self, mock_stdout):
        # 测试绿色打印函数
        print_green("测试文本")
        # 验证输出包含ANSI颜色代码和文本
        self.assertEqual(mock_stdout.getvalue(), "\033[32m测试文本\033[0m\n")
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_print_yellow(self, mock_stdout):
        # 测试黄色打印函数
        print_yellow("测试文本")
        # 验证输出包含ANSI颜色代码和文本
        self.assertEqual(mock_stdout.getvalue(), "\033[33m测试文本\033[0m\n")
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_print_red(self, mock_stdout):
        # 测试红色打印函数
        print_red("测试文本")
        # 验证输出包含ANSI颜色代码和文本
        self.assertEqual(mock_stdout.getvalue(), "\033[31m测试文本\033[0m\n")
    
    @patch('src.gewechat.utils.terminal_printer.print_green')
    @patch('src.gewechat.utils.terminal_printer.qrcode.QRCode')
    def test_make_and_print_qr(self, mock_qrcode_class, mock_print_green):
        # 设置模拟对象
        mock_qrcode = MagicMock()
        mock_qrcode_class.return_value = mock_qrcode
        
        # 调用被测试的函数
        test_url = "https://example.com"
        make_and_print_qr(test_url)
        
        # 验证调用
        mock_print_green.assert_any_call("请扫描下方二维码登录")
        mock_print_green.assert_any_call(f"也可以访问下方链接获取二维码:\nhttps://api.qrserver.com/v1/create-qr-code/?data={test_url}")
        
        # 验证QRCode操作
        mock_qrcode.add_data.assert_called_once_with(test_url)
        mock_qrcode.make.assert_called_once()
        mock_qrcode.print_ascii.assert_called_once_with(invert=True)

if __name__ == '__main__':
    unittest.main() 