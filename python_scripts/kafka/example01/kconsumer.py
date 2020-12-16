#!/data/exec/python/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/1 11:35
# @Author  : YuZhiYi
# @Email   : yuzhiyi@54.com
# https://kafka-python.readthedocs.io/en/master/apidoc/KafkaConsumer.html
# https://github.com/dpkp/kafka-python
from kafka import KafkaConsumer

consumer = KafkaConsumer('my_favorite_topic')
for msg in consumer:
    print(msg)

# join a consumer group for dynamic partition assignment and offset commits
from kafka import KafkaConsumer

consumer = KafkaConsumer('my_favorite_topic', group_id='my_favorite_group')
for msg in consumer:
    print(msg)

# manually assign the partition list for the consumer
from kafka import TopicPartition

consumer = KafkaConsumer(bootstrap_servers='localhost:1234')
consumer.assign([TopicPartition('foobar', 2)])
msg = next(consumer)


# Deserialize msgpack-encoded values
consumer = KafkaConsumer(value_deserializer=msgpack.loads)
consumer.subscribe(['msgpackfoo'])
for msg in consumer:
    assert isinstance(msg.value, dict)

# Access record headers. The returned value is a list of tuples
# with str, bytes for key and value
for msg in consumer:
    print(msg.headers)

# Get consumer metrics
metrics = consumer.metrics()
