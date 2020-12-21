#!/data/exec/python/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/1 11:47
# @Author  : YuZhiYi
# @Email   : yuzhiyi@54.com
import json
import random
import uuid
import time
from kafka import KafkaProducer,TopicPartition
kafka_cluster = ['192.168.10.181:9092','192.168.10.182:9092','192.168.10.183:9092']

client_uuid = 'producer_' + str(uuid.uuid4())


producer = KafkaProducer(bootstrap_servers=kafka_cluster, # bootstrap_servers 指定broker的地址清单
                         key_serializer=str.encode, #  键的序列化器 默认为None 传入 b'key'
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'),# 值的序列化器 默认为None 传入 b'value'
                         batch_size=16384,  # 多个消息被放在同一批次 按字节数计算而不是消息个数
                         compression_type='gzip', # 压缩算法 snappy gzip lz4
                         acks=1, #acks 0 不会等待服务器响应 1 只要收到群首消息就认为成功响应 all 当所有同步副本接收消息，生产者才会收到服务器的响应
                         retries=3, # 重试次数 默认间隔 100ms
                         client_id = client_uuid,  # 服务器用来识别消息来源
                         max_in_flight_requests_per_connection = 1, # 如果分片内的消息要保证有序 则视为1
                         )
try:
    for _ in range(50):
    # send(topic, value=None, key=None, headers=None, partition=None, timestamp_ms=None)
    # 同步发送 返回一个 Future对象，使用get方法进行同步等待  并返回一个RecordMetadata对象

        topic = 'foobar'
        key = str(random.choice('abcdefghijklmnopqrstuvwxyz'))
        msg = {'hello':random.randint(1,100),'uuid':str(uuid.uuid4()),'producer_uuid':client_uuid}
        the_future = producer.send(topic=topic,value=msg,key=key)
        time.sleep(random.randint(1,5))
        the_future.get(timeout=3)
        record_meta_data = the_future.value
        s = '''
            ----------------------------------------------------
            topic: %s
            partition: %s
            offset: %s
            timestamp: %s
            serialized_key_size: %s
            serialized_value_size: %s
            log_start_offset: %s
            checksum: %s
            
            '''
        print(s % (record_meta_data.topic,
                   record_meta_data.partition,
                   record_meta_data.offset,
                   record_meta_data.timestamp,
                   record_meta_data.serialized_key_size,
                   record_meta_data.serialized_value_size,
                   record_meta_data.log_start_offset,
                   record_meta_data.checksum))
except Exception as e:
    print(e)
finally:
    producer.close()
