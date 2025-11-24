import json
import requests
from typing import Dict, Optional
from dataclasses import dataclass
from src.Config import config
import os 

class OCRClient:
    def __init__(self, app_id: str, secret_code: str):
        self.app_id = app_id
        self.secret_code = secret_code

    def recognize(self, file_content: bytes, options: dict) -> str:
        # 构建请求参数
        params = {}
        for key, value in options.items():
            params[key] = str(value)

        # 设置请求头
        headers = {
            "x-ti-app-id": self.app_id,
            "x-ti-secret-code": self.secret_code,
            # 方式一：读取本地文件
            "Content-Type": "application/octet-stream"
            # 方式二：使用URL方式
            # "Content-Type": "text/plain"
        }

        # 发送请求
        response = requests.post(
            f"https://api.textin.com/ai/service/v1/pdf_to_markdown",
            params=params,
            headers=headers,
            data=file_content
        )

        # 检查响应状态
        response.raise_for_status()
        return response.text

def convert(target_pdf : str, target_dir : str):
    # 创建客户端实例
    client = OCRClient(config.textin_app_id, config.textin_secret_key)

    # 读取图片文件
    # 方式一：读取本地文件
    with open(target_pdf, "rb") as f:
        file_content = f.read()

    # 设置转换选项
    options = dict(
        apply_document_tree=1,
        apply_image_analysis=0,
        apply_merge=1,
        catalog_details=1,
        dpi=144,
        formula_level=1,
        get_excel=1,
        get_image="both",
        markdown_details=1,
        page_count=1000,
        page_details=1,
        page_start=1,
        paratext_mode="annotation",
        parse_mode="scan",
        raw_ocr=0,
        table_flavor="md",
    )

    try:
        response = client.recognize(file_content, options)
        
        # 保存完整的JSON响应到result.json文件
        with open("result.json", "w", encoding="utf-8") as f:
            f.write(response)
        
        # 解析JSON响应以提取markdown内容
        json_response = json.loads(response)
        if "result" in json_response and "markdown" in json_response["result"]:
            markdown_content = json_response["result"]["markdown"]
            with open(os.path.join(target_dir, "result.md"), "w", encoding="utf-8") as f:
                f.write(markdown_content)
    
    except Exception as e:
        print(f"Error: {e}")