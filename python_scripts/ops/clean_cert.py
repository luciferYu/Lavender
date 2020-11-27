#!/data/exec/python/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/11/23 11:43
# @Author  : YuZhiYi
# @Email   : yuzhiyi@54.com
# 编写一个清理证书的脚本
import json
import os
import dns.resolver
import datetime
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ssl.v20191205 import ssl_client, models
# 导入可选配置类
region = "ap-shanghai"

# 从环境变量 获取账户
J_Tencent_Account = os.environ.get("Tencent_Account")
Tencent_Account = json.loads(J_Tencent_Account)
master_account = None
for account in Tencent_Account['tecent_cloud_accounts']:
    if account['account'] == '主账号':
        master_account = account

print(master_account)


try:
    cred = credential.Credential(master_account['secretId'], master_account['secretKey'])
    httpProfile = HttpProfile()
    httpProfile.endpoint = "ssl.tencentcloudapi.com"

    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    client = ssl_client.SslClient(cred, "", clientProfile)

    req = models.DescribeCertificatesRequest()
    params = {

    }
    req.from_json_string(json.dumps(params))

    resp = client.DescribeCertificates(req)
    certs = json.loads(resp.to_json_string())
    certs["Certificates"].sort(key=lambda x:x['StatusName'])
    title = '|'.join(certs["Certificates"][0].keys())
    print(title)
    for cer in certs["Certificates"]:
        print(cer)
except TencentCloudSDKException as err:
    print(err)