import json
import requests
import re
import base64
from typing import Tuple
from src.Config import config


class OCRClient:
    def __init__(self, app_id: str, secret_code: str):
        self.app_id = app_id
        self.secret_code = secret_code
        self.content_type = {
            'file': "application/octet-stream",
            'url': "text/plain"
        }
    
    
    def getContentFromType(self, url : str, url_type : str) -> bytes :
        if url_type == 'file':
            with open(url, 'rb') as f:
                result = f.read()
                return result
        else :
            return url
    
    def recognize(self, url: str, url_type : str, options: dict) -> str:
        # 构建请求参数
        params = {}
        for key, value in options.items():
            params[key] = str(value)    

        # 设置请求头
        headers = {
            "x-ti-app-id": self.app_id,
            "x-ti-secret-code": self.secret_code,
            "Content-Type": self.content_type[url_type]
        }

        # 发送请求
        response = requests.post(
            f"https://api.textin.com/ai/service/v1/pdf_to_markdown",
            params=params,
            headers=headers,
            data=self.getContentFromType(url, url_type)
        )

        # 检查响应状态
        response.raise_for_status()
        return response.text

# 提取所有表格的markdown形式
def get_tables_md(json_result : str) -> str :
    json_response = json.loads(json_result)
    if "result" in json_response and "markdown" in json_response["result"]:
        markdown_content = json_response["result"]["markdown"]
        tables = re.findall(r'(?:\|.*\n)+', markdown_content)
        tables_md = '\n'.join(tables)        

# 提取所有表格的json形式  
def get_tables_json(json_result : str) -> str :
    tables_json = []
    json_response = json.loads(json_result)
    if "result" in json_response and 'pages' in json_response["result"]:
        for page in json_response["result"]["pages"]:
            for block in page.get("structured", []):
                if block.get("type") == "table":
                    tables_json.append(block)

    return tables_json

# 从返回的Json结果提取所有表格以excel 二进制数据的形式  
def get_tables_by_excel_bytes(json_result : str) -> bytes: 
    json_response = json.loads(json_result)
    if "result" in json_response and "excel_base64" in json_response["result"]:
        excel_base64 = json_response["result"]["excel_base64"]
        excel_bytes = base64.b64decode(excel_base64)
        return excel_bytes

# 从返回的Json结果获取目录树json格式
def get_catalog_tree(json_result : str) :
    json_response = json.loads(response)
    if "result" in json_response and "catalog" in json_response["result"]:
        catalog = json_response["result"]["catalog"]
        return catalog

# 从返回的Json结果获取markdown全文
def get_markdown(json_result : str) -> str:
    json_response = json.loads(json_result)
    if "result" in json_response and "markdown" in json_response["result"]:
        markdown_content = json_response["result"]["markdown"]
        return markdown_content

# 获取返回的json字符串
def parse(url : str, url_type : str, params : dict) -> Tuple[str, str]:
    client = OCRClient(config.textin_app_id, config.textin_secret_key)
    
    options = dict( # 传入的配置
        dpi=144,
        get_image="objects",
        markdown_details=1,
        page_count=3,
        parse_mode="auto",
        table_flavor="html"
    )
    
    options.update(params)
    
    try:
        response = client.recognize(url, url_type, options)

        return response
    except Exception as e:
        print(f"Error: {e}")
