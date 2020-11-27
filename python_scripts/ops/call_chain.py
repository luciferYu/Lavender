#!/data/exec/python/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/11/24 15:04
# @Author  : YuZhiYi
# @Email   : yuzhiyi@54.com
import json
import os

import requests
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile



class TCloud(object):
    def __init__(self):
        self.region = "ap-shanghai"
        # 从环境变量 获取账户
        self.J_DNSPOD = os.environ.get("DNSPOD")
        self.DNSPOD = json.loads(self.J_DNSPOD)
        self.J_Tencent_Account = os.environ.get("Tencent_Account")
        Tencent_Account = json.loads(self.J_Tencent_Account)
        self.master_account = None
        self.domain_account = None
        for account in Tencent_Account['tecent_cloud_accounts']:
            if account['account'] == '主账号':
                self.master_account = account
            elif account['account'] == '域名账号':
                self.domain_account = account
        print(self.master_account)
        print(self.domain_account)

    def get_all_clb_set(self):
        from tencentcloud.clb.v20180317 import clb_client, models
        try:
            cred = credential.Credential(self.master_account['secretId'], self.master_account['secretKey'])
            httpProfile = HttpProfile()
            httpProfile.endpoint = "clb.tencentcloudapi.com"

            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            client = clb_client.ClbClient(cred, self.region, clientProfile)

            req = models.DescribeLoadBalancersRequest()
            params = {
                "Limit": 100,
                "Offset": 0
            }
            req.from_json_string(json.dumps(params))

            resp = client.DescribeLoadBalancers(req)
            ret = json.loads(resp.to_json_string())
            return ret

        except TencentCloudSDKException as err:
            print(err)

    def get_all_instance_set(self):
        # todo 此处没有处理超过100个实例的逻辑
        from tencentcloud.cvm.v20170312 import cvm_client, models
        try:
            cred = credential.Credential(self.master_account['secretId'], self.master_account['secretKey'])
            httpProfile = HttpProfile()
            httpProfile.endpoint = "cvm.tencentcloudapi.com"

            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            client = cvm_client.CvmClient(cred, self.region, clientProfile)

            req = models.DescribeInstancesRequest()
            params = {
                "Limit": 100
            }
            req.from_json_string(json.dumps(params))
            resp = client.DescribeInstances(req)
            ret = json.loads(resp.to_json_string())
            return ret

        except TencentCloudSDKException as err:
            print(err)

    def get_classical_clb_target(self, id):
        from tencentcloud.clb.v20180317 import clb_client, models
        try:
            cred = credential.Credential(self.master_account['secretId'], self.master_account['secretKey'])
            httpProfile = HttpProfile()
            httpProfile.endpoint = "clb.tencentcloudapi.com"

            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            client = clb_client.ClbClient(cred, self.region, clientProfile)

            req = models.DescribeClassicalLBTargetsRequest()
            params = {
                "LoadBalancerId": id,
                "Limit": 100,
                "Offset": 0
            }
            req.from_json_string(json.dumps(params))

            resp = client.DescribeClassicalLBTargets(req)
            ret = json.loads(resp.to_json_string())
            return ret

        except TencentCloudSDKException as err:
            print(err)

    def get_classical_clb_listeners(self, id):
        from tencentcloud.clb.v20180317 import clb_client, models
        try:
            cred = credential.Credential(self.master_account['secretId'], self.master_account['secretKey'])
            httpProfile = HttpProfile()
            httpProfile.endpoint = "clb.tencentcloudapi.com"

            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            client = clb_client.ClbClient(cred, self.region, clientProfile)

            req = models.DescribeClassicalLBListenersRequest()
            params = {
                "LoadBalancerId": id,
                "Limit": 100,
                "Offset": 0
            }
            req.from_json_string(json.dumps(params))

            resp = client.DescribeClassicalLBListeners(req)
            ret = json.loads(resp.to_json_string())
            return ret
        except TencentCloudSDKException as err:
            print(err)

    def get_domain_name_list(self):
        from tencentcloud.domain.v20180808 import domain_client, models
        try:
            cred = credential.Credential(self.domain_account['secretId'], self.domain_account['secretKey'])
            httpProfile = HttpProfile()
            httpProfile.endpoint = "domain.tencentcloudapi.com"

            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            client = domain_client.DomainClient(cred, "", clientProfile)

            req = models.DescribeDomainNameListRequest()
            params = {
                "Limit": 100,
                "Offset": 0
            }
            req.from_json_string(json.dumps(params))

            resp = client.DescribeDomainNameList(req)
            ret = json.loads(resp.to_json_string())
            return ret
        except TencentCloudSDKException as err:
            print(err)

    def get_domain_resolve(self, dn):
        from tencentcloud.sslpod.v20190605 import sslpod_client, models
        try:
            cred = credential.Credential(self.domain_account['secretId'], self.domain_account['secretKey'])
            httpProfile = HttpProfile()
            httpProfile.endpoint = "sslpod.tencentcloudapi.com"

            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            client = sslpod_client.SslpodClient(cred, "", clientProfile)

            req = models.ResolveDomainRequest()
            params = {
                "Domain": dn
            }
            req.from_json_string(json.dumps(params))

            resp = client.ResolveDomain(req)
            ret = json.loads(resp.to_json_string())
            return ret
        except TencentCloudSDKException as err:
            print(err)

    def get_domain_recode_list(self, dn='00joy.com', rtype=None, sdn=None):
        url = 'https://dnsapi.cn/Record.List'
        login_token = self.DNSPOD['ID'] + ',' + self.DNSPOD['Token']
        data = {
            'domain': dn,
            'login_token': login_token,
            'format': 'json',
            'lang': 'cn',
            'error_on_empty': 'no',
            'length': 3000,
        }
        if sdn:
            data['sub_domain'] = sdn
        if rtype:
            data['record_type'] = rtype

        header = {
            'user-agent': 'Lavender Client/1.0.0'
        }
        try:
            resp = requests.post(url, headers=header, data=data)
            ret = json.loads(resp.text, encoding='utf-8')
            return ret
        except Exception as e:
            raise e

    def run(self):
        # all_clb_set = self.get_all_clb_set()
        # print(all_clb_set)
        # for clb in all_clb_set['LoadBalancerSet']:
        #     if clb['Forward'] == 0:
        #         print('传统型CLB')
        #         print(clb['LoadBalancerId'])
        #         target = self.get_classical_clb_target(clb['LoadBalancerId'])
        #         listeners = self.get_classical_clb_listeners(clb['LoadBalancerId'])
        #         print(target)
        #         print(listeners)

        domain_list = self.get_domain_name_list()
        for domain in domain_list['DomainSet']:
            # print(domain['DomainName'])
            print(domain)
            # ret = self.get_domain_resolve(domain['DomainName'])
            # print(ret)

    def get_call_chain_by_domain(self, dn):
        pass

    def get_all_ip_assosiation(self):
        ret = {}
        # 1 从域名解析 获取IP 与域名对应关系
        ips_list = []
        for domain in ['00joy.com', '54.com', 'nikugame.com']:
            domain_list = self.get_domain_recode_list(dn=domain, rtype='A')
            for ip in domain_list['records']:
                ip['name'] += '.' + domain_list['domain']['name']
            ips_list += domain_list['records']
        ips_list.sort(key=lambda x: x['value'])  # 排序
        print(ips_list)
        for dn in ips_list:
            if dn['enabled'] == '1':
                if dn['value'] not in ret.keys():
                    ret[dn['value']] = {'domain': [dn['name'], ]}
                else:
                    ret[dn['value']]['domain'].append(dn['name'])

                    # print(dn['name'], dn['type'], dn['value'])

        # 2 从负载均衡 获取IP 与 负载均衡对应关系
        clbs = self.get_all_clb_set()
        for k, v in ret.items():
            for clb in clbs['LoadBalancerSet']:
                if k in clb['LoadBalancerVips']:
                    if 'clb' not in ret[k].keys():
                        ret[k]['clb'] = [clb]
                    else:
                        ret[k]['clb'].append(clb)
                    # 添加 clb 关联的主机
                    if clb['Forward'] == 0:  # 传统型elb
                        targets = self.get_classical_clb_target(clb['LoadBalancerId'])
                        if 'clb_targets' not in ret[k].keys():
                            ret[k]['clb_targets'] = [targets]
                        else:
                            ret[k]['clb_targets'].append(targets)
                    elif clb['Forward'] == 1:  # 普通负载均衡
                        # todo
                        pass
                    else:
                        pass

            # 3 从云服务器 获取IP 与 实例对应关系
            all_instances_set = self.get_all_instance_set()
            for ins in all_instances_set['InstanceSet']:
                #print(ins)
                #if (k in ins['PrivateIpAddresses']) or (k in ins['PublicIpAddresses']):
                if ins['PrivateIpAddresses']:
                    if k in ins['PrivateIpAddresses']:
                        if 'ins' not in ret[k].keys():
                            ret[k]['ins'] = [ins]
                        else:
                            ret[k]['ins'].append(ins)
                if ins['PublicIpAddresses']:
                    if k in ins['PublicIpAddresses']:
                        if 'ins' not in ret[k].keys():
                            ret[k]['ins'] = [ins]
                        else:
                            ret[k]['ins'].append(ins)

            # 打印结果
            print(k)
            for x, y in v.items():
                print(x, y)
            print('-' * 60)
        # 4 从云数据库 获取IP 与 实例对应关系
        # 5 从云缓存 获取IP 与实例对应关系
        with open('ip_list.json', 'w', encoding='utf-8') as f:
            json.dump(ret, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    tc = TCloud()
    # tc.run()
    tc.get_all_ip_assosiation()
