#!/data/exec/python/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/1 11:47
# @Author  : YuZhiYi
# @Email   : yuzhiyi@54.com
import json
from kafka import KafkaConsumer
from kafka.coordinator.assignors.range import RangePartitionAssignor
from kafka.coordinator.assignors.roundrobin import RoundRobinPartitionAssignor
kafka_cluster = ['192.168.10.181:9092','192.168.10.182:9092','192.168.10.183:9092']
#consumer = KafkaConsumer('foobar',group_id='my_favorite_group',bootstrap_servers=kafka_cluster)
topic = 'foobar'
consumer = KafkaConsumer(#topic,
                         bootstrap_servers=kafka_cluster,
                         key_deserializer=bytes.decode,  # 键的反序列化器 默认为None 传入 b'key'
                         value_deserializer=lambda v: json.loads(v.decode('utf-8')),  # 值的反序列化器 默认为None 传入 b'value'
                         group_id = 'mygroup', # 消费组

                         auto_offset_reset= 'latest', # 当各分区下有已提交的offset时，从提交的offset开始消费；无提交的offset时，消费新产生的该分区下的数据 ，
                         #auto_offset_reset='earliest',   # earliest 当各分区下有已提交的offset时，从提交的offset开始消费；无提交的offset时，从头开始消费

                         # kafka 在收到消费者请求时候 要么返回fetch_min_bytes 的数据 要么在fetch_max_wait_ms时间到达时返回
                         fetch_min_bytes = 1048576, # 单位Mb
                         fetch_max_wait_ms = 500,

                         max_partition_fetch_bytes = 1048576, # 服务器从每个分区里返回消费者的最大字节数 必须大于max.message.size

                         session_timeout_ms = 10000, #指定消费者可以多久不发送心跳
                         heartbeat_interval_ms = 3000, # 指定了发送心跳的频率 该值一般为 session_timeout_ms 的三分之一

                         enable_auto_commit = True, # 设置是否自动提交偏移量
                         auto_commit_interval_ms = 5000, # 如果 enable_auto_commit 设置为True 则为自动提交的间隔

                         # 默认分配策略
                         # RangePartitionAssignor 该策略把主题若干个连续的分区分配给消费者
                         # RoundRobinPartitionAssignor 改策略把主题的所有分区逐个分配给消费者
                         partition_assignment_strategy =  [RangePartitionAssignor,RoundRobinPartitionAssignor ],

                         client_id = 'zhiyi_cnsm', # broker 用它来标识客户端发送过来的消息 通常用在日志度量指标的配额里

                         #socket 在读写数据时用到的TCP缓冲区大小 如果生产者和消费者的broker在不同数据中心内，可以适当增大这个值
                         receive_buffer_bytes = 32768,
                         send_buffer_bytes = 131072
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
