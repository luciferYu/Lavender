#!/data/exec/python/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/1 11:34
# @Author  : YuZhiYi
# @Email   : yuzhiyi@54.com
# https://kafka-python.readthedocs.io/en/master/apidoc/KafkaProducer.html
#https://github.com/dpkp/kafka-python
from kafka import KafkaProducer
kafka_cluster = ['192.168.10.181:9092','192.168.10.182:9092','192.168.10.183:9092',]
producer = KafkaProducer(bootstrap_servers=kafka_cluster)
for _ in range(100):
    producer.send('foobar', b'some_message_bytes')


# Block until a single message is sent (or timeout)
future = producer.send('foobar', b'another_message')
result = future.get(timeout=60)

# Block until all pending messages are at least put on the network
# NOTE: This does not guarantee delivery or success! It is really
# only useful if you configure internal batching using linger_ms
producer.flush()

# Use a key for hashed-partitioning
producer.send('foobar', key=b'foo', value=b'bar')

# Serialize json messages
import json
producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'))
producer.send('fizzbuzz', {'foo': 'bar'})

# Serialize string keys
producer = KafkaProducer(key_serializer=str.encode)
producer.send('flipflap', key='ping', value=b'1234')

#Compress messages
producer = KafkaProducer(compression_type='gzip')
for i in range(1000):
    producer.send('foobar', b'msg %d' % i)


# Include record headers. The format is list of tuples with string key
# and bytes value.
producer.send('foobar', value=b'c29tZSB2YWx1ZQ==', headers=[('content-encoding', b'base64')])

# Get producer performance metrics
metrics = producer.metrics()