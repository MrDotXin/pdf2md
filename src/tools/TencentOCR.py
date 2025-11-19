# -*- coding: utf-8 -*-

import sys
import os
from dotenv import load_dotenv
load_dotenv(".env", override=True)

import base64
import json
import types
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.lkeap.v20240522 import lkeap_client, models


def submit():
    try:
        # 密钥信息从环境变量读取，需要提前在环境变量中设置 TENCENTCLOUD_SECRET_ID 和 TENCENTCLOUD_SECRET_KEY
        # 使用环境变量方式可以避免密钥硬编码在代码中，提高安全性
        # 生产环境建议使用更安全的密钥管理方案，如密钥管理系统(KMS)、容器密钥注入等
        # 请参见：https://cloud.tencent.com/document/product/1278/85305
        # 密钥可前往官网控制台 https://console.cloud.tencent.com/cam/capi 进行获取
        cred = credential.Credential(os.getenv("TENCENTCLOUD_SECRET_ID"), os.getenv("TENCENTCLOUD_SECRET_KEY"))
        # 使用临时密钥示例
        # cred = credential.Credential("SecretId", "SecretKey", "Token")
        # 实例化一个http选项，可选的，没有特殊需求可以跳过
        httpProfile = HttpProfile()
        httpProfile.endpoint = "lkeap.tencentcloudapi.com"

        # 实例化一个client选项，可选的，没有特殊需求可以跳过
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        # 实例化要请求产品的client对象,clientProfile是可选的
        client = lkeap_client.LkeapClient(cred, "ap-guangzhou", clientProfile)

        # 读取文件并转换为 base64 字符串
        with open('./ReAct.pdf', 'rb') as file:
            file_data = file.read()
            file_base64 = base64.b64encode(file_data).decode('utf-8')
        
        # 实例化一个请求对象,每个接口都会对应一个request对象
        req = models.CreateReconstructDocumentFlowRequest()
        params = {
            "FileBase64": file_base64,
            "FileType": "pdf",
            "Config": {
                "TableResultType": "0",
                "ResultType": "3",
            }
        }
        
        req.from_json_string(json.dumps(params))

        # 返回的resp是一个CreateReconstructDocumentFlowResponse的实例，与请求对象对应
        resp = client.CreateReconstructDocumentFlow(req)
        # 输出json格式的字符串回包
        print(resp.to_json_string())

    except TencentCloudSDKException as err:
        print(err)


def query(taskId : str):
    try:
        # 密钥信息从环境变量读取，需要提前在环境变量中设置 TENCENTCLOUD_SECRET_ID 和 TENCENTCLOUD_SECRET_KEY
        # 使用环境变量方式可以避免密钥硬编码在代码中，提高安全性
        # 生产环境建议使用更安全的密钥管理方案，如密钥管理系统(KMS)、容器密钥注入等
        # 请参见：https://cloud.tencent.com/document/product/1278/85305
        # 密钥可前往官网控制台 https://console.cloud.tencent.com/cam/capi 进行获取
        cred = credential.Credential(os.getenv("TENCENTCLOUD_SECRET_ID"), os.getenv("TENCENTCLOUD_SECRET_KEY"))
        # 使用临时密钥示例
        # cred = credential.Credential("SecretId", "SecretKey", "Token")
        # 实例化一个http选项，可选的，没有特殊需求可以跳过
        httpProfile = HttpProfile()
        httpProfile.endpoint = "lkeap.tencentcloudapi.com"

        # 实例化一个client选项，可选的，没有特殊需求可以跳过
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        # 实例化要请求产品的client对象,clientProfile是可选的
        client = lkeap_client.LkeapClient(cred, "ap-guangzhou", clientProfile)

        # 实例化一个请求对象,每个接口都会对应一个request对象
        req = models.GetReconstructDocumentResultRequest()
        params = {
            "TaskId": taskId
        }
        req.from_json_string(json.dumps(params))

        # 返回的resp是一个GetReconstructDocumentResultResponse的实例，与请求对象对应
        resp = client.GetReconstructDocumentResult(req)
        # 输出json格式的字符串回包
        print(resp.to_json_string())

    except TencentCloudSDKException as err:
        print(err)
        
if __name__ == '__main__':
    query("2e4b86761763534470288")