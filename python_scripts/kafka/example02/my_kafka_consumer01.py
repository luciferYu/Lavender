#!/data/exec/python/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/1 11:47
# @Author  : YuZhiYi
# @Email   : yuzhiyi@54.com
import json
from kafka import KafkaConsumer
kafka_cluster = ['192.168.10.181:9092','192.168.10.182:9092','192.168.10.183:9092']
#consumer = KafkaConsumer('foobar',group_id='my_favorite_group',bootstrap_servers=kafka_cluster)
topic = 'foobar'
consumer = KafkaConsumer(#topic,
                         bootstrap_servers=kafka_cluster,
                         key_deserializer=bytes.decode,  # 键的反序列化器 默认为None 传入 b'key'
                         value_deserializer=lambda v: json.loads(v.decode('utf-8')),  # 值的反序列化器 默认为None 传入 b'value'
                         group_id = 'mygroup' # 消费组
                         )

consumer.subscribe(topics=(topic,))  # 订阅主题
#metrics = consumer.metrics()
# print(metrics)
try:
    count = 0
    for msg in consumer:
        count += 1
        #print(msg.topic,msg.partition,msg.offset,msg.key,msg.value)
        print('第%s条消息：主题 %s 分区 %s offset %s 键 %s 消息内容 %s' % (count,msg.topic,msg.partition,msg.offset,msg.key,msg.value))
except Exception as e:
    print(e)
finally:
    consumer.close()
