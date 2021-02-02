#!/data/exec/python/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2021/1/7 10:41
# @Author  : YuZhiYi
# @Email   : yuzhiyi@54.com
#Let’s quickly tour operations to create a table, load some data, and fetch it back.
# https://altinitydb.medium.com/clickhouse-and-python-getting-to-know-the-clickhouse-driver-client-47d6c1c42b8f
from clickhouse_driver import Client

client = Client('192.168.10.181',
                user='default',
                password='com.0123',
                secure=False,
                verify=False,
                database='yuzhiyi_test',
                compression=True)

# client.execute('''CREATE TABLE iris_from_csv (
#                sepal_length Decimal32(2), sepal_width Decimal32(2),
#                petal_length Decimal32(2), petal_width Decimal32(2),
#                species String) ENGINE = MergeTree
#                PARTITION BY species
#                ORDER BY (species)''')

client.execute('''INSERT INTO iris_from_csv (sepal_length, sepal_width, petal_length, petal_width, species) 
                  VALUES''', [(5.1, 3.7, 1.5, 0.4, 'Iris-setosa'), (4.6, 3.6, 1.0, 0.2, 'Iris-setosa')])

result = client.execute('''SELECT COUNT(*), species FROM iris_from_csv 
                        WHERE petal_length > toDecimal32(3.4, 2) 
                        GROUP BY species ORDER BY species''')
print(result)
