#!/data/exec/python/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/1 11:47
# @Author  : YuZhiYi
# @Email   : yuzhiyi@54.com
import time
import json
from kafka import KafkaConsumer,TopicPartition
kafka_cluster = ['192.168.10.181:9092','192.168.10.182:9092','192.168.10.183:9092']
topic = 'foobar'
consumer = KafkaConsumer(group_id='mygroup02',
                         bootstrap_servers=kafka_cluster,
                         key_deserializer=bytes.decode,  # 键的反序列化器 默认为None 传入 b'key'
                         value_deserializer=lambda v: json.loads(v.decode('utf-8')),  # 值的反序列化器 默认为None 传入 b'value'
                         max_poll_records = 500 # 单次调用poll返回的最大记录数
                         )

consumer.subscribe(topics=(topic,))  # 订阅主题

# 或者

# 指定主题和分区和offset
# partitions = [ TopicPartition(topic=topic,partition=i) for i in range(16)]
# consumer.assign(partitions=partitions)
# for i in range(16):
#     consumer.seek(partitions[i],0)   # 分区[i],offset


index = 0
count = 0
try:
    while True:
        msg = consumer.poll(timeout_ms=5, max_records=None, update_offsets=True) # poll()方法 总是返回由生产者写入kafka但还没有被消费者读取过的记录
        index += 1
        for topic_partion in msg.values():
            for consumer_record in topic_partion:
                count += 1
                print('第%s批次消息 第%s条消息：主题 %s 分区 %s offset %s 键 %s 消息内容 %s' % (index,count,consumer_record.topic, consumer_record.partition, consumer_record.offset, consumer_record.key, consumer_record.value))
        time.sleep(2)

except Exception as e:
    print(e)
finally:
    consumer.close()
