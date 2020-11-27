#!/data/exec/python/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/11/20 9:56
# @Author  : YuZhiYi
# @Email   : yuzhiyi@54.com
# 编写一个脚本，将腾讯云不同账号下的费用汇总插入倒数据库中，运行一次插入一次
# 导入对应产品模块的client models。
import json
import os
import datetime
import pymysql
from tencentcloud.billing.v20180709 import billing_client, models
from tencentcloud.common import credential
# 导入可选配置类
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
region = "ap-shanghai"
#
# 数据库
# CREATE TABLE `tencent_balance` (
#   `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
#   `dt` datetime DEFAULT NULL COMMENT '日期时间',
#   `account` varchar(64) DEFAULT NULL COMMENT '账号',
#   `balance` int(11) DEFAULT NULL COMMENT '余额',
#   PRIMARY KEY (`id`)
# ) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4

# 每15分钟采集一次的crontab 把环境变量 exprot到了 /root/.bashrc
# */10 * * * * source /root/.bashrc && /data/scripts/cost.py >> /data/logs/cost.log 2>&1 &

class SqlHelp(object):
    def __init__(self, DATABASE):
        self.conn = pymysql.connect(host=DATABASE['HOST'], user=DATABASE['USER'], password=DATABASE['PASSWORD'],
                                    db=DATABASE['NAME'],port=DATABASE['PORT'],
                                    charset='utf8')
        self.cur = self.conn.cursor()

    def __del__(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()

    def selectone(self, sql, sql_params):
        try:
            row = self.cur.execute(sql, sql_params)
            ret = self.cur.fetchone()
        except Exception as e:
            raise e
        else:
            return ret

    def selectmany(self, sql, sql_params):
        try:
            row = self.cur.execute(sql, sql_params)
            ret = self.cur.fetchall()
        except Exception as e:
            raise e
        else:
            return ret

    def insert(self, sql, sql_params):
        try:
            row = self.cur.execute(sql, sql_params)
        except Exception as e:
            self.conn.rollback()
            raise e
        else:
            self.conn.commit()
            return row

    def insert_many(self, sql, sql_params):
        try:
            row = self.cur.executemany(sql, sql_params)
        except Exception as e:
            self.conn.rollback()
            raise e
        else:
            self.conn.commit()
            return row

def get_account_balance(TENCENTCLOUD_SDK):
    cred = credential.Credential(TENCENTCLOUD_SDK["secretId"], TENCENTCLOUD_SDK["secretKey"])
    httpProfile = HttpProfile()
    httpProfile.reqMethod = "GET"  # post请求(默认为post请求)
    httpProfile.reqTimeout = 30  # 请求超时时间，单位为秒(默认60秒)
    httpProfile.endpoint = "billing.tencentcloudapi.com"  # 指定接入地域域名(默认就近接入)
    # 实例化一个client选项，可选的，没有特殊需求可以跳过。
    clientProfile = ClientProfile()
    clientProfile.signMethod = "TC3-HMAC-SHA256"  # 指定签名算法
    # clientProfile.language = "en-US"
    clientProfile.language = "zh-CN"
    clientProfile.httpProfile = httpProfile

    bclient = billing_client.BillingClient(credential=cred, region=region, profile=clientProfile)
    req = models.DescribeAccountBalanceRequest()
    # req.Limit = 100
    # req.Offset = 0
    resp = bclient.DescribeAccountBalance(req)
    return resp.Balance


if __name__ == "__main__":
    # 从环境变量 获取账户
    J_Tencent_Account = os.environ.get("Tencent_Account")
    Tencent_Account = json.loads(J_Tencent_Account)
    J_DB_OPS = os.environ.get("DB_OPS")
    DB = json.loads(J_DB_OPS)
    # 实例化sql工具类
    sql_help = SqlHelp(DB)

    for TENCENTCLOUD_SDK in Tencent_Account["tecent_cloud_accounts"]:
        balance = get_account_balance(TENCENTCLOUD_SDK)
        print("%s %s %s" % (TENCENTCLOUD_SDK['account'],balance,datetime.datetime.now()))
        sql = '''insert into tencent_balance(dt,account,balance) values (%s,%s,%s)''' # 插入数据表
        sql_params = (datetime.datetime.now(),TENCENTCLOUD_SDK['account'],balance)
        sql_help.insert(sql,sql_params)


