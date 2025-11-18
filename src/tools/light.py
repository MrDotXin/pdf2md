import requests
import time
import os
from typing import Optional, Union, BinaryIO, Tuple
import threading


class ConversionPromise:
    def __init__(self, client, task_id: str, target_format: str):
        self.client = client
        self.task_id = task_id
        self.target_format = target_format
        self._result = None
        self._completed = False
        self._error = None

    def store(self, file_path: str, timeout: int = 30, poll_interval: int = 1) -> bool:
        """
        阻塞等待转换完成并将结果保存到指定文件路径
        
        Args:
            file_path: 保存文件的路径
            timeout: 最大等待时间（秒），默认30秒
            poll_interval: 轮询间隔（秒），默认1秒
            
        Returns:
            bool: 转换是否成功
        """
        if self._completed:
            if self._error:
                raise Exception(f"Conversion failed: {self._error}")
            return self._download_result(file_path)
        
        # 轮询获取结果
        start_time = time.time()
        while time.time() - start_time < timeout:
            result = self.client.get_conversion_result(self.task_id)
            
            print(f"watting... {result.get('status')}")
            if result.get('state') == 1:  
                self._completed = True
                self._result = result
                return self._download_result(file_path)
            elif result.get('state') == -1: 
                self._completed = True
                self._error = result.get('message', 'Unknown error')
                raise Exception(f"Conversion failed: {self._error}")
            
            time.sleep(poll_interval)
        
        raise TimeoutError(f"Conversion timeout after {timeout} seconds")

    def _download_result(self, file_path: str) -> bool:
            """下载转换结果到指定路径"""
            if not self._result:
                return False
                
            download_url = self._result.get('file')
            if not download_url:
                return False
            
            response = requests.get(download_url, stream=True)
            if response.status_code == 200:
                # 确保目录存在
                os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
                
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                return True
            return False


class lightPDF:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://techsz.aoscdn.com/api/tasks/document/conversion"
    
    def convert(self, 
                file: Union[str, BinaryIO], 
                target_format: str = 'md', 
                password: Optional[str] = None,
                page_range: Optional[Tuple[int, int]] = None) -> ConversionPromise:
        """
        开始文档转换任务
        
        Args:
            file: 文件路径或文件内容(bytes)
            target_format: 目标格式，默认'md'
            password: 文档密码（如果有）
            page_range: 转换页码范围，如'1-5,8,10-12'
            
        Returns:
            ConversionPromise: 转换承诺对象，可以调用store方法保存结果
        """
        # 准备请求数据
        data = {'format': target_format}
        
        # 准备文件
        if not isinstance(file, str):
            should_close=True
            
        files = {'file': file}
        if password :
            data['password'] = password
        if page_range :
            page_begin, page_end = page_range
            data['page_range'] = f"{page_begin}-{page_end}"
            
        try:
            # 创建转换任务
            print('创建任务中...')
            response = requests.post(
                self.base_url,
                headers={'X-API-KEY': self.api_key},
                data=data,
                files=files
            )
            
            if response.status_code != 200:
                raise Exception(f"API request failed: {response.text}")
            
            result = response.json()
            task_id = result.get('data', {}).get('task_id')
            print(f"成功创建任务! task_id {task_id}")
            if not task_id:
                raise Exception(f"Failed to get task ID: {result}")
            
            return ConversionPromise(self, task_id, target_format)
            
        finally:
            # 确保文件被关闭
            if should_close and 'files' in locals():
                files['file'].close()
    
    def get_conversion_result(self, task_id: str) -> dict:
        """
        获取转换任务结果
        
        Args:
            task_id: 任务ID
            
        Returns:
            dict: 转换结果
        """
        url = f"{self.base_url}/{task_id}"
        response = requests.get(
            url,
            headers={'X-API-KEY': self.api_key}
        )
        
        if response.status_code != 200:
            return {'status': 'error', 'message': f"HTTP {response.status_code}"}
        
        return response.json().get('data', {})