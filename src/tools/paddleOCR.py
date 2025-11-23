import requests
import aspose.pdf as ap
import base64
import io
import urllib
from src.Config import config

API_KEY = config.baidu_api_key
SECRET_KEY = config.baidu_secret_key

def post() :

    def main():
            
        url = "https://aip.baidubce.com/rest/2.0/brain/online/v2/paddle-vl-parser/task?access_token=" + get_access_token()


        # Load PDF document
        document = ap.Document("E:\\Book\\实用API\\PDFToMd\\ReAct.pdf")

        # Save PDF into memory stream
        memory_stream = io.BytesIO()
        document.save(memory_stream)

        # Convert memory stream to byte array
        byte_array = memory_stream.getvalue()

        # Convert to Base64 string
        base64_result = base64.b64encode(byte_array).decode("utf-8")

        payload=f'file_data={urllib.parse.quote(base64_result)}&file_name=ReAct.pdf&analysis_chart=False'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }
        
        response = requests.request("POST", url, headers=headers, data=payload.encode("utf-8"))
        
        response.encoding = "utf-8"
        print(response.json()['result']['task_id'])
        task_id = response.json()['result']['task_id']
        return task_id

    def get_access_token():
        """
        使用 AK，SK 生成鉴权签名（Access Token）
        :return: access_token，或是None(如果错误)
        """
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
        return str(requests.post(url, params=params).json().get("access_token"))

    main()

def fetch(taskid : str) :
    import requests

    def main():
            
        url = "https://aip.baidubce.com/rest/2.0/brain/online/v2/paddle-vl-parser/task/query?access_token=" + get_access_token()
        
        payload=f'task_id={taskid}'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }
        
        response = requests.request("POST", url, headers=headers, data=payload.encode("utf-8"))
        
        response.encoding = "utf-8"
        print(response.text)
        

    def get_access_token():
        """
        使用 AK，SK 生成鉴权签名（Access Token）
        :return: access_token，或是None(如果错误)
        """
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
        return str(requests.post(url, params=params).json().get("access_token"))

    main()

