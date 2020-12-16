#!/data/exec/python/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/1 11:47
# @Author  : YuZhiYi
# @Email   : yuzhiyi@54.com
import time
import json
from kafka import KafkaConsumer
from pprint import pprint
from kafka import TopicPartition
kafka_cluster = ['192.168.10.181:9092','192.168.10.182:9092','192.168.10.183:9092']
consumer = KafkaConsumer(group_id='yuzhiyi',bootstrap_servers=kafka_cluster)
consumer.assign([TopicPartition(topic='Login',partition=0),TopicPartition(topic='Login',partition=1)])
print(consumer.partitions_for_topic('Login'))
print(consumer.assignment())
consumer.seek(TopicPartition(topic='Login',partition=1),0)
for msg in consumer:
    #recv = "%s:%d:%d: key=%s value=%s" % (msg.topic, msg.partition, msg.offset, msg.key, msg.value)
    #print(recv)
    pprint(json.loads(msg.value))
