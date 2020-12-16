#!/data/exec/python/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/1 11:47
# @Author  : YuZhiYi
# @Email   : yuzhiyi@54.com
from kafka import KafkaConsumer
from kafka import TopicPartition
kafka_cluster = ['192.168.10.181:9092','192.168.10.182:9092','192.168.10.183:9092']
consumer = KafkaConsumer('test',group_id='my_favorite_group',bootstrap_servers=kafka_cluster)
for msg in consumer:
    print(msg)
    #print(msg.topic,msg.partition,msg.offset,msg.key,msg.value)