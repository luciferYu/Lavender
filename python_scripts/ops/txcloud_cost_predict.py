#!/data/exec/python/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/24 16:00
# @Author  : YuZhiYi
# @Email   : yuzhiyi@54.com
import os
import datetime
import time
import json
import pymysql
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException

def all_balance(account):
    from tencentcloud.billing.v20180709 import billing_client, models
    try:
        cred = credential.Credential(account["secretId"], account["secretKey"])
        httpProfile = HttpProfile()
        httpProfile.endpoint = "billing.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = billing_client.BillingClient(cred, "", clientProfile)

        req = models.DescribeAccountBalanceRequest()
        params = {

        }
        req.from_json_string(json.dumps(params))

        resp = client.DescribeAccountBalance(req)
        # print(resp.to_json_string())
        allBalance = json.loads(resp.to_json_string())

        return allBalance.get('Balance')
    except TencentCloudSDKException as err:
        print(err)

def sqlDescribeDBInstances(account):
    # 输入 ins_dict 操作  输出 ins_dict
    from tencentcloud.cdb.v20170320 import cdb_client, models
    try:
        cred = credential.Credential(account["secretId"], account["secretKey"])
        httpProfile = HttpProfile()
        httpProfile.endpoint = "cdb.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = cdb_client.CdbClient(cred, "ap-shanghai", clientProfile)

        req = models.DescribeDBInstancesRequest()
        params = {

        }
        req.from_json_string(json.dumps(params))

        resp = client.DescribeDBInstances(req)
       # print(resp.to_json_string())
        sql_inp_dict = json.loads(resp.to_json_string())

        # print(inp_dict)
        #sql_list = []
        return sql_inp_dict
    except TencentCloudSDKException as err:
            print(err)

def get_db_price(god_num,mem,vol,account):
    from tencentcloud.cdb.v20170320 import cdb_client, models
    try:
        cred = credential.Credential(account["secretId"], account["secretKey"])
        httpProfile = HttpProfile()
        httpProfile.endpoint = "cdb.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = cdb_client.CdbClient(cred, "ap-shanghai", clientProfile)

        req = models.DescribeDBPriceRequest()
        params = {
            "Zone": "ap-shanghai-2",
            "GoodsNum": god_num,
            'Memory': mem,
            "Volume": vol,
            "PayType": "PRE_PAID",
            "Period": 1
        }
        #print(params)
        req.from_json_string(json.dumps(params))

        resp = client.DescribeDBPrice(req)
        retsql = json.loads(resp.to_json_string())
        return retsql
    except TencentCloudSDKException as err:
        print(err)

#获取redis实例ID，到期时间
def red_DescribeInstances(account):
    from tencentcloud.redis.v20180412 import redis_client, models
    try:
        cred = credential.Credential(account["secretId"], account["secretKey"])
        httpProfile = HttpProfile()
        httpProfile.endpoint = "redis.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = redis_client.RedisClient(cred, "ap-shanghai", clientProfile)

        req = models.DescribeInstancesRequest()
        params = {

        }
        req.from_json_string(json.dumps(params))

        resp = client.DescribeInstances(req)
        red_inp_dict = json.loads(resp.to_json_string())
        # for ins in red_inp_dict['InstanceSet']:
        #     red_id = ins['InstanceId']
        #     red_DeadlineTime= ins['DeadlineTime']
        #     print(red_id,red_DeadlineTime)
        #print(resp.to_json_string())
        return red_inp_dict
    except TencentCloudSDKException as err:
        print(err)

#获取redis续费价格
def get_redis_price(id,account):
    from tencentcloud.redis.v20180412 import redis_client, models
    try:
        cred = credential.Credential(account["secretId"], account["secretKey"])
        httpProfile = HttpProfile()
        httpProfile.endpoint = "redis.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = redis_client.RedisClient(cred, "ap-shanghai", clientProfile)

        req = models.InquiryPriceRenewInstanceRequest()
        params = {
            "Period": 1,
            "InstanceId": id
        }
        #print(params)
        req.from_json_string(json.dumps(params))

        resp = client.InquiryPriceRenewInstance(req)
        redis_resp=json.loads(resp.to_json_string())
        #print(resp.to_json_string())
        return redis_resp
    except TencentCloudSDKException as err:
        print(err)

#价格查询
def Price_inquiry(ins_id,account,region):
    from tencentcloud.cvm.v20170312 import cvm_client, models
    try:
        cred = credential.Credential(account["secretId"], account["secretKey"])
        httpProfile = HttpProfile()
        httpProfile.endpoint = "cvm.tencentcloudapi.com"
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = cvm_client.CvmClient(cred, region, clientProfile)

        req = models.InquiryPriceRenewInstancesRequest()

        params = {
            "InstanceIds": [ins_id, ],
            "InstanceChargePrepaid": {
                "Period": 1,
                "RenewFlag": "NOTIFY_AND_AUTO_RENEW"
            },
            "RenewPortableDataDisk": True
        }
        req.from_json_string(json.dumps(params))
        resp = client.InquiryPriceRenewInstances(req)
        resp_dict = json.loads(resp.to_json_string())
        price_sh = int(resp_dict['Price']['InstancePrice']['DiscountPrice']) *100
        return price_sh
    except TencentCloudSDKException as err:
        print(err)

# 接收价格获取实例ID及到期时间
def Renewal_inquiry(account,region):
    from tencentcloud.cvm.v20170312 import cvm_client, models
    try:
        cred = credential.Credential(account["secretId"], account["secretKey"])
        httpProfile = HttpProfile()
        httpProfile.endpoint = "cvm.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = cvm_client.CvmClient(cred, region, clientProfile)
        req = models.DescribeInstancesRequest()
        params = {
            "Filters": [
                {
                    "Values": ["PREPAID"],
                    "Name": "instance-charge-type"
                }
            ]
        }
        req.from_json_string(json.dumps(params))

        resp = client.DescribeInstances(req)

        ret = json.loads(resp.to_json_string())

        return ret
    except TencentCloudSDKException as err:
        print(err)

# #价格查询
# def Price_inquiry_frankfur(ins_id,account):
#     from tencentcloud.cvm.v20170312 import cvm_client, models
#     try:
#         cred = credential.Credential(account["secretId"], account["secretKey"])
#         httpProfile = HttpProfile()
#         httpProfile.endpoint = "cvm.tencentcloudapi.com"
#         clientProfile = ClientProfile()
#         clientProfile.httpProfile = httpProfile
#         client = cvm_client.CvmClient(cred, "eu-frankfurt", clientProfile)
#
#         req = models.InquiryPriceRenewInstancesRequest()
#
#         params = {
#             "InstanceIds": [ins_id, ],
#             "InstanceChargePrepaid": {
#                 "Period": 1,
#                 "RenewFlag": "NOTIFY_AND_AUTO_RENEW"
#             },
#             "RenewPortableDataDisk": True
#         }
#         req.from_json_string(json.dumps(params))
#         resp = client.InquiryPriceRenewInstances(req)
#         resp_dict = json.loads(resp.to_json_string())
#         price_int = int(resp_dict['Price']['InstancePrice']['DiscountPrice']) * 100
#         return price_int
#     except TencentCloudSDKException as err:
#         print(err)
#
#
# # 接收价格获取实例ID及到期时间
# def Renewal_inquiry_frankfur(account):
#     from tencentcloud.cvm.v20170312 import cvm_client, models
#     try:
#         cred = credential.Credential(account["secretId"], account["secretKey"])
#         httpProfile = HttpProfile()
#         httpProfile.endpoint = "cvm.tencentcloudapi.com"
#
#         clientProfile = ClientProfile()
#         clientProfile.httpProfile = httpProfile
#         client = cvm_client.CvmClient(cred, "eu-frankfurt", clientProfile)
#         req = models.DescribeInstancesRequest()
#         params = {
#             "Filters": [
#                 {
#                     "Values": ["PREPAID"],
#                     "Name": "instance-charge-type"
#                 }
#             ]
#         }
#         req.from_json_string(json.dumps(params))
#
#         resp = client.DescribeInstances(req)
#
#         ret = json.loads(resp.to_json_string())
#
#         return ret
#     except TencentCloudSDKException as err:
#         print(err)





global cur
global conn

def connect():
    try:
        # 建立数据库连接
        global conn
        J_DB_OPS = os.environ.get("DB_OPS")
        DB = json.loads(J_DB_OPS)
        conn = pymysql.connect(host=DB['HOST'], port=DB['PORT'],user=DB['USER'], password=DB['PASSWORD'], db=DB['NAME'], charset='utf8')
    except Exception as e:
        print("无法链接数据库连接" + e)
    else:
        print("数据库连接成功")

    # 获取游标对象
    global cur
    cur = conn.cursor()

def clean():
    global cur
    global conn
    # SQL语句更新数据
    sql = 'truncate table tencent_balance_predict'
    try:
        # 执行SQL语句
        cur.execute(sql)
        # 提交到数据库执行
        conn.commit()
        print("删除数据成功")

    except Exception as e:
        print("删除数据失败：case%s"%e)
        #发生错误时回滚
        conn.rollback()

def write_data(data):
    global cur
    global conn
    try:
        sql = 'insert into tencent_balance_predict(dt,account,balance_predict) values (%s,%s,%s);'
        sql_params = (data[0], '黑暗信仰余额预算', data[1])
        try:
            cur.execute(sql, sql_params)
        except Exception as e:
            conn.rollback()
            raise e
        else:
            conn.commit()
    except Exception as e:
        raise e


def close():
    global cur
    global conn
    cur.close()
    conn.close()


if __name__ == '__main__':
    # 1 1 * * * source /root/.bashrc && /data/scripts/txcloud_cost_predict.py  >> /data/logs/cost_predict.log 2>&1 &
    t_start = time.perf_counter()
    # 从环境变量 获取账户
    J_Tencent_Account = os.environ.get("Tencent_Account")
    Tencent_Account = json.loads(J_Tencent_Account)
    Tencent_Account = Tencent_Account['tecent_cloud_accounts'][0]

    # 日期相关
    today_time = datetime.datetime.now()
    # 获取到计算价格并存入
    today_Banlace = all_balance(Tencent_Account)
    # 获取sql详情
    ins_dict = sqlDescribeDBInstances(Tencent_Account)

    price_predict_list = [] #结果
    # 计算未来三十天需要金额
    for day in range(30):
        #t1 = time.perf_counter()
        after_time = datetime.timedelta(day)
        # 日期转换为str类型
        test_time_str = str(today_time + after_time)
        # 计算redis价格
        for ins_redis in red_DescribeInstances(Tencent_Account)['InstanceSet']:
            if ins_redis['DeadlineTime'][:10] == test_time_str[:10]:
                price_redisdict = get_redis_price(ins_redis['InstanceId'], Tencent_Account)
                price_sql = price_redisdict['Price']
                today_Banlace = today_Banlace - price_sql
        #t2 = time.perf_counter()
        # 计算SQL价格
        for ins_sql in ins_dict['Items']:
            if ins_sql['DeadlineTime'][:10] == test_time_str[:10]:
                price_sqldict = get_db_price(ins_sql['Cpu'], ins_sql['Memory'], ins_sql['Volume'], Tencent_Account)
                today_Banlace = today_Banlace - price_sqldict['Price']
        #t3 = time.perf_counter()
        # 计算服务器价格
        for region in ["ap-shanghai","eu-frankfurt"]:
            for ins_ser_sh in Renewal_inquiry(Tencent_Account,region)["InstanceSet"]:
                if ins_ser_sh['ExpiredTime'][:10] == test_time_str[:10]:
                    price_server_sh = Price_inquiry(ins_ser_sh['InstanceId'],Tencent_Account,region)
                    today_Banlace = today_Banlace - price_server_sh
        #t4 = time.perf_counter()

        #print(t2-t1,t3-t2,t4-t3)
        print((test_time_str[:10], round(today_Banlace / 100, 2)))
        price_predict_list.append((test_time_str[:10], round(today_Banlace / 100, 2)))

    connect()
    clean()
    for price_predict in price_predict_list:
        write_data(price_predict)
    else:
        close()
        print('数据插入完成')

    t_end = time.perf_counter()
    t_all = t_end - t_start
    print('总共耗时%s秒' % t_all)