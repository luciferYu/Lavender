#!/data/exec/python/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2021/1/7 10:55
# @Author  : YuZhiYi
# @Email   : yuzhiyi@54.com
'''
https://segmentfault.com/a/1190000023091291
目前在ClickHouse中，按照特点可以将表引擎大致分成6个系列，分别是合并树、外部存储、内存、文件、接口和其他，每一个系列的表引擎都有着独自的特点与使用场景。在它们之中，最为核心的当属MergeTree系列，因为它们拥有最为强大的性能和最广泛的使用场合。
大家应该已经知道了MergeTree有两层含义：
其一，表示合并树表引擎家族；
其二，表示合并树家族中最基础的MergeTree表引擎。
而在整个家族中，除了基础表引擎MergeTree之外，常用的表引擎还有ReplacingMergeTree、SummingMergeTree、AggregatingMergeTree、CollapsingMergeTree和VersionedCollapsingMergeTree。每一种合并树的变种，在继承了基础MergeTree的能力之后，又增加了独有的特性。其名称中的“合并”二字奠定了所有类型MergeTree的基因，它们的所有特殊逻辑，都是在触发合并的过程中被激活的。在本章后续的内容中，会逐一介绍它们的特点以及使用方法。

MergeTree
MergeTree作为家族系列最基础的表引擎，提供了数据分区、一级索引和二级索引等功能。

数据TTL
TTL即Time To Live，顾名思义，它表示数据的存活时间。在MergeTree中，可以为某个列字段或整张表设置TTL。当时间到达时，如果是列字段级别的TTL，则会删除这一列的数据；如果是表级别的TTL，则会删除整张表的数据；如果同时设置了列级别和表级别的TTL，则会以先到期的那个为主。无论是列级别还是表级别的TTL，都需要依托某个DateTime或Date类型的字段，通过对这个时间字段的INTERVAL操作，来表述TTL的过期时间，例如：
'''
import datetime
import random
import time
from clickhouse_driver import Client

client = Client('192.168.10.181',
                user='default',
                password='com.0123',
                secure=False,
                verify=False,
                database='yuzhiyi_test',
                compression=True)

client.execute('''DROP TABLE IF EXISTS yuzhiyi_test.ttl_table_v1''')

# 字段TTL值 过期了会将字段变为默认值  测试后发现不生效
sql_column = '''CREATE TABLE IF NOT EXISTS yuzhiyi_test.ttl_table_v1 (
    id String,
    create_time DateTime,
    code String DEFAULT '' TTL create_time + INTERVAL 10 SECOND,
    types UInt8 DEFAULT 0 TTL create_time + INTERVAL 10 SECOND
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(create_time)
ORDER BY id ;'''

#ttl_table_v2整张表被设置了TTL，当触发TTL清理时，那些满足过期时间的数据行将会被整行删除。
# 同样，表级别的TTL也支持修改，修改的方法如下：
# 测试后生效
sql_table = '''CREATE TABLE IF NOT EXISTS yuzhiyi_test.ttl_table_v1(
    id String,
    create_time DateTime,
    code String ,
    types UInt8
) ENGINE = MergeTree
PARTITION BY toYYYYMM(create_time)
ORDER BY create_time
TTL create_time + INTERVAL 20 SECOND ;'''


#client.execute(sql_column)
client.execute(sql_table)
for i in range(10):

    d = ((str(i),datetime.datetime.now(),random.choice('ABCDabcd'),random.randint(1,5)),)
    print(d)
    client.execute('''insert into yuzhiyi_test.ttl_table_v1(id,create_time,code,types) values''',d )
    time.sleep(2)
# clickhouse-client -h
#
#  127.0.0.1 -d   yuzhiyi_test -m -u default  --password com.0123
# ALTER TABLE tt1_table_v2 MODIFY TTL create_time + INTERVAL 3 DAY;



while True:
    #ret = client.execute('''OPTIMIZE TABLE yuzhiyi_test.ttl_table_v1;''')  # 触发合并
    ret = client.execute('''OPTIMIZE TABLE yuzhiyi_test.ttl_table_v1 FINAL;''') # 触发所有分区合并
    print(ret)

    print('DO OPTIMIZE TABLE')
    result = client.execute('''select * from yuzhiyi_test.ttl_table_v1;''')
    for row in result:
        print(row)
    print('-' * 50)

    time.sleep(2)



