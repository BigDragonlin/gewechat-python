import unittest
import json
import os
import requests
import base64
from src.gewechat.utils.dify import Dify
from src.gewechat.utils.config import config


class TestDifyAPI(unittest.TestCase):
    def setUp(self):
        self.url = "https://api.dify.ai/v1/completion-messages"
        self.headers = {
            "Authorization": "Bearer app-d3VRFwb42JXy3i7GbG4YIGuz",
            "Content-Type": "application/json",
        }

    def test_dify_api(self):
        data = {
            "inputs": {"user_zodiac": "摩羯座", "today_date": "2021-09-01"},
            "response_mode": "blocking",
            "user": "abc-123",
        }
        response = requests.post(self.url, headers=self.headers, json=data)
        if response.status_code != 200:
            print(f"API调用失败: {response.status_code}, 错误: {response.text}")
        else:
            print(response.json())

    def test_class_dify(self):
        base_url = config["dify"]["api_url"]
        api_key = config["dify"]["fortone_teller"]["api_key"]
        api_type = config["dify"]["fortone_teller"]["api_type"]
        dify = Dify(base_url, api_type, api_key)

        data = {
            "inputs": {"user_zodiac": "摩羯座", "today_date": "2021-09-01"},
            "response_mode": "blocking",
            "user": "abc-123",
        }

        try:
            response = dify.get_response(data)
            if isinstance(response, dict):
                if "data" in response and "outputs" in response["data"]:
                    print("输出内容:", response["data"]["outputs"])
                else:
                    print("完整响应:", response)
            else:
                print("非字典响应:", response)
        except Exception as e:
            print(f"调用Dify API时出错: {e}")

    def test_class_dify_error(self):
        base_url = config["dify"]["api_url"]
        api_key = config["dify"]["fortone_teller"]["api_key"]
        api_type = config["dify"]["fortone_teller"]["api_type"]
        dify = Dify(base_url, api_type, api_key)
        data = {
            "inputs": {"user_zodiac": "摩羯座", "today_date": "2021-09-01"},
            "response_mode": "error",
            "user": "abc-123",
        }
        with self.assertRaises(RuntimeError):
            dify.get_response(data)

    # 测试fangshuren
    def test_class_dify_fangshuren(self):
        base_url = config["dify"]["api_url"]
        api_key = config["dify"]["fangshuren"]["api_key"]
        api_type = config["dify"]["fangshuren"]["api_type"]
        dify = Dify(base_url, api_type, api_key)

        # 上传图片获取ID
        user_id = "abc-123"
        image_path = "fangshuren.jpg"
        upload_file_id = self.upload_file(image_path, user_id, api_key)

        # 使用正确的数据结构构建请求
        data = {
            "inputs": {
                "images": {  # 这里的"images"应该是您在Dify应用中定义的变量名
                    "transfer_method": "local_file",
                    "upload_file_id": upload_file_id,
                    "type": "image",
                }
            },
            "response_mode": "blocking",
            "user": user_id,
        }

        response = dify.get_response(data)
        print(response)

    def upload_file(self, file_path, user, api_key):
        """上传文件到Dify并获取upload_file_id"""
        upload_url = f"{config['dify']['api_url']}/files/upload"
        headers = {
            "Authorization": f"Bearer {api_key}",
        }

        try:
            with open(file_path, "rb") as file:
                files = {
                    "file": (
                        os.path.basename(file_path),
                        file,
                        "image/jpeg",
                    )  # 根据实际图片类型调整
                }
                data = {"user": user}

                response = requests.post(
                    upload_url, headers=headers, files=files, data=data
                )
                if response.status_code == 201:  # 201 表示创建成功
                    return response.json().get("id")  # 获取上传的文件 ID
                else:
                    raise RuntimeError(
                        f"文件上传失败，状态码: {response.status_code}, 响应: {response.text}"
                    )
        except Exception as e:
            raise RuntimeError(f"上传文件时发生错误: {str(e)}")

    # 测试灵签
    def test_class_dify_lingqian(self):
        base_url = config["dify"]["api_url"]
        api_key = config["dify"]["lingqian"]["api_key"]
        api_type = config["dify"]["lingqian"]["api_type"]
        dify = Dify(base_url, api_type, api_key)

        # 简单请求无需文件上传
        data = {
            "inputs": {},  # 灵签应用不需要输入参数
            "response_mode": "blocking",
            "user": "abc-123",
        }

        response = dify.get_response(data)
        # 在Dify 1.0中，可能需要调整响应解析方式
        try:
            # 尝试新的返回格式
            text_output = response.get("data", {}).get("outputs", {}).get("text", {})
            if not text_output:
                # 可能是旧格式或其他格式
                text_output = response.get("answer", {})

            formatted_str = ""
            if isinstance(text_output, dict):
                for key, value in text_output.items():
                    formatted_str += f"{key}：{value}\n"
            else:
                formatted_str = str(text_output)

            print("response______________")
            print(formatted_str)
        except Exception as e:
            print(f"解析响应时出错: {e}")
            print("原始响应:", response)

    # 测试运气
    def test_class_dify_yunqi(self):
        base_url = config["dify"]["api_url"]
        api_key = config["dify"]["yunqi"]["api_key"]
        api_type = config["dify"]["yunqi"]["api_type"]
        dify = Dify(base_url, api_type, api_key)

        # Dify 1.0中的正确输入格式
        data = {
            "inputs": {
                "xingzuo": "摩羯座",  # 保持原有输入参数
            },
            "response_mode": "blocking",
            "user": "abc-123",
        }

        response = dify.get_response(data)
        # 在Dify 1.0中，可能需要调整响应解析方式
        try:
            # 尝试新的返回格式
            result = response.get("data", {}).get("outputs", {}).get("result")
            if result is None:
                # 尝试其他可能的路径
                result = response.get("workflow_run_id", "未找到结果")

            print("response______________")
            print(result)
        except Exception as e:
            print(f"解析响应时出错: {e}")
            print("原始响应:", response)


if __name__ == "__main__":
    unittest.main()
