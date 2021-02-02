#!/data/exec/python/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2021/1/7 10:30
# @Author  : YuZhiYi
# @Email   : yuzhiyi@54.com
from clickhouse_driver import Client

client = Client('192.168.10.181',
                user='default',
                password='com.0123',
                secure=False,
                verify=False,
                database='yuzhiyi_test',
                compression=True)

result = client.execute('SELECT now(),version()')
print('%s %s' % (type(result),result))

for t in result:
    print('row: %s:%s' % (type(t),t))
    for v in t:
        print('column: %s:%s' % (type(v),v))