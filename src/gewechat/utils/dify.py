import requests
import json
import os
import base64


class Dify:
    def __init__(self, api_url, api_type, api_key):
        self.api_url = f"{api_url.rstrip('/')}/{api_type.lstrip('/')}"
        self.api_key = api_key
        self.headers = {"Authorization": f"Bearer {self.api_key}"}
        self.base_url = api_url.rstrip("/")

    def upload_file(self, file_path):
        """上传文件到Dify服务器，返回上传文件的ID"""
        upload_url = f"{self.base_url}/files/upload"

        # 准备文件对象
        file_type = self._get_file_type(file_path)
        files = {
            "file": (os.path.basename(file_path), open(file_path, "rb"), file_type)
        }

        # 准备表单数据
        form_data = {"user": "test-user"}  # 用户标识

        # 发送请求
        response = requests.post(
            upload_url,
            headers=self.headers,  # 只需要Authorization头
            files=files,
            data=form_data,
        )

        # 直接解析响应内容
        response_data = response.json()

        # 检查响应中是否包含id字段
        if "id" in response_data:
            return response_data["id"]  # 返回上传的文件ID
        else:
            # 只有当响应中没有id字段时才报错
            raise RuntimeError(f"文件上传失败: {response.text}")

    def _get_file_type(self, file_path):
        """根据文件后缀获取文件类型"""
        ext = os.path.splitext(file_path)[1].lower()

        # 图片类型
        if ext in [".jpg", ".jpeg", ".png", ".gif", ".webp"]:
            return "image/jpeg" if ext in [".jpg", ".jpeg"] else f"image/{ext[1:]}"
        # 文档类型
        elif ext in [".pdf"]:
            return "application/pdf"
        elif ext in [".txt"]:
            return "text/plain"
        # 默认类型
        else:
            return "application/octet-stream"

    def get_response(self, data):
        """
        发送请求到Dify API，处理文件上传和API调用
        采用两步法：
        1. 先上传文件获取文件ID
        2. 然后在JSON请求中包含文件ID
        """
        # 复制一份数据，避免修改原始数据
        json_data = data.copy()

        # 处理文件上传
        if "inputs" in json_data and "images" in json_data["inputs"]:
            image_path = json_data["inputs"]["images"]

            # 如果是文件路径，上传文件获取ID
            if isinstance(image_path, str) and os.path.isfile(image_path):
                # 上传文件获取ID
                file_id = self.upload_file(image_path)

                # 更新inputs中的images为文件ID
                json_data["inputs"]["images"] = file_id

                # 添加文件列表（使用files关键字）
                json_data["files"] = [
                    {
                        "type": "image",
                        "transfer_method": "local_file",
                        "upload_file_id": file_id,
                    }
                ]

        # 设置头部并确保Content-Type为application/json
        headers = self.headers.copy()
        headers["Content-Type"] = "application/json"

        # 发送请求（使用json参数确保Content-Type正确）
        response = requests.post(self.api_url, headers=headers, json=json_data)

        if response.status_code == 200:
            return response.json()
        else:
            raise RuntimeError(response.text)
