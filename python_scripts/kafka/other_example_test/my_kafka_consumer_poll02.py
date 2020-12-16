#!/data/exec/python/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/1 11:47
# @Author  : YuZhiYi
# @Email   : yuzhiyi@54.com
import time
from kafka import KafkaConsumer,TopicPartition
kafka_cluster = ['192.168.10.181:9092','192.168.10.182:9092','192.168.10.183:9092']
consumer = KafkaConsumer(group_id='yuzhiyi02',bootstrap_servers=kafka_cluster)
#consumer.subscribe(topics=('test',))
consumer.assign([TopicPartition(topic='test',partition=0),TopicPartition(topic='test',partition=1)])
consumer.seek(TopicPartition(topic='test',partition=0),0)
index = 0
while True:
    msg = consumer.poll(timeout_ms=5) # 从kafka里获取消息
    #print(msg)
    for m in msg.values():
        print(m)
    time.sleep(2)
    index += 1
    print('--------poll index is %s----------' % index)