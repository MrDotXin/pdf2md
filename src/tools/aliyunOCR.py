# -*- coding: utf-8 -*-
import sys
import os
from dotenv import load_dotenv
load_dotenv(".env", override=True)

from typing import List
from alibabacloud_docmind_api20220711.client import Client as docmind_api20220711Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_docmind_api20220711 import models as docmind_api20220711_models
from alibabacloud_tea_util.client import Client as UtilClient
from alibabacloud_tea_util import models as util_models
from alibabacloud_credentials.client import Client as CredClient

import json

def create_client() -> docmind_api20220711Client:
    """   
    @return: Client
    @throws Exception
    """
    # 调用接口时，程序直接访问凭证，读取您的访问密钥（即AccessKey）并自动完成鉴权。
    # 运行本示例前，请先完成步骤二：配置身份认证。
    # 本示例使用默认配置文件方式，通过配置Credentials文件创建默认的访问凭证。
    # 使用默认凭证初始化Credentials Client。
    cred=CredClient()
    config = open_api_models.Config(
        # 通过Credentials获取配置中的AccessKey ID
        access_key_id=cred.get_credential().access_key_id,
        # 通过Credentials获取配置中的AccessKey Secret
        access_key_secret=cred.get_credential().access_key_secret
    )
    # 访问的域名
    config.endpoint = f'docmind-api.cn-hangzhou.aliyuncs.com'
    return docmind_api20220711Client(config)


def submit(): 
    client = create_client()
    request = docmind_api20220711_models.SubmitDocStructureJobAdvanceRequest(
        # file_url_object : 本地文件流
        file_url_object=open("./ReAct.pdf", "rb"),
        # file_name_extension : 文件后缀格式。与文件名二选一
        file_name_extension='pdf'
    )
    runtime = util_models.RuntimeOptions()
    try:
        # 复制代码运行请自行打印 API 的返回值
        response = client.submit_doc_structure_job_advance(request, runtime)

        print(response.body)       
    except Exception as error:
        # 如有需要，请打印 error
        UtilClient.assert_as_string(error.message)

def query() :
    client = create_client()
    request = docmind_api20220711_models.GetDocStructureResultRequest(
        # id :  任务提交接口返回的id
        id='docmind-20251119-8f55721f9de34a04b3a7fd8c0b98e42e'
    )
    try:
        # 复制代码运行请自行打印 API 的返回值
        response = client.get_doc_structure_result(request)
        # API返回值格式层级为 body -> data -> 具体属性。可根据业务需要打印相应的结果。获取属性值均以小写开头
        # 获取异步任务处理情况,可根据response.body.completed判断是否需要继续轮询结果
        # 获取返回结果。建议先把response.body.data转成json，然后再从json里面取具体需要的值。
        print(json.dumps(response.body.data))        
    except Exception as error:
        # 如有需要，请打印 error
        UtilClient.assert_as_string(error.message)
        
if __name__ == '__main__':
    query()