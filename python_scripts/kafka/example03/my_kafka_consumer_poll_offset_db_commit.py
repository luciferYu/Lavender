#!/data/exec/python/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/1 11:47
# @Author  : YuZhiYi
# @Email   : yuzhiyi@54.com
import time
import json
import os
import uuid
import pymysql
from kafka import KafkaConsumer,TopicPartition
from kafka.structs import TopicPartition,OffsetAndMetadata
from kafka.consumer.subscription_state import ConsumerRebalanceListener







class SaveOffsetOnRebalance(ConsumerRebalanceListener):
    def __init__(self,my_kafka_consumer):
        super(SaveOffsetOnRebalance,self).__init__()
        self.my_kafka_consumer = my_kafka_consumer

    def on_partitions_revoked(self, revoked):
        # revoked (list of TopicPartition): the partitions that were assigned to the consumer on the last rebalance
        self.my_kafka_consumer.commit_db_transaction()

    def on_partitions_assigned(self, assigned):
        #  assigned (list of TopicPartition): the partitions assigned to the consumer (may include partitions that were previously assigned)
        for topic_partition in assigned:
            # print(topic_partition,self.get_offset_from_db(topic_partition))
            self.my_kafka_consumer.consumer.seek(topic_partition, self.my_kafka_consumer.get_offset_from_db(topic_partition))


class MyKafkaConsumer(object):
    def __init__(self,bootstrap_servers,group_id=None,):
        self. client_uuid = 'consumer_' + str(uuid.uuid4())
        self.consumer = KafkaConsumer(
                                 bootstrap_servers=bootstrap_servers,
                                 group_id=group_id,
                                 key_deserializer=bytes.decode,  # 键的反序列化器 默认为None 传入 b'key'
                                 value_deserializer=lambda v: json.loads(v.decode('utf-8')),
                                 # 值的反序列化器 默认为None 传入 b'value'
                                 max_poll_records=500,  # 单次调用poll返回的最大记录数
                                 enable_auto_commit=False,  # 设置是否自动提交偏移量 自动提交虽然方便，但是没有留余地来避免重复消息处理
                                 client_id=self.client_uuid,  # broker 用它来标识客户端发送过来的消息 通常用在日志度量指标的配额里
                                 )
        DATABASE = json.loads(os.environ.get('DB_OPS'))
        self.conn = pymysql.connect(host=DATABASE['HOST'], port=DATABASE['PORT'], user=DATABASE['USER'],
                               password=DATABASE['PASSWORD'],
                               db=DATABASE['NAME'],
                               charset='utf8')
        self.cur = self.conn.cursor()
        print('consumer is init...')

    def __del__(self):
        self.consumer.close()
        self.cur.close()
        self.conn.close()
        print('consumer is closed')

    def get_offset_from_db(self,topic_partition):
        try:
            sql = 'select poffset from kafka_consumer_offset where ktopic=%s and kpartition=%s;'
            sql_params = (topic_partition.topic, topic_partition.partition)
            row = self.cur.execute(sql, sql_params)
            if row:
                offset = self.cur.fetchone()[0]
                return offset
            else:
                # 数据库如果没有这个topic的offset 就新建一条记录，把offset设为0
                offset = 0
                sql = 'insert into kafka_consumer_offset(ktopic,kpartition,poffset) values (%s,%s,%s);'
                sql_params = (topic_partition.topic, topic_partition.partition, 0)
                try:
                    self.cur.execute(sql, sql_params)
                except Exception as e:
                    self.conn.rollback()
                    raise e
                else:
                    #self.conn.commit()
                    return offset
        except Exception as e:
            raise e

    def process_recode(self,record):
        print('主题 %s 分区 %s offset %s 键 %s 消息内容 %s' % (
            record.topic, record.partition, record.offset,record.key, record.value))

    def store_recode_in_db(self,record):
        sql = 'insert into kafka_msg(ktopic,kpartition,poffset,mkey,mvalue) values (%s,%s,%s,%s,%s);'
        sql_params = (record.topic, record.partition, record.offset,record.key, json.dumps(record.value))
        try:
            self.cur.execute(sql, sql_params)
        except Exception as e:
            raise e

    def store_offset_in_db(self,record):
        sql = 'update kafka_consumer_offset set poffset = %s where ktopic = %s and kpartition = %s;'
        sql_params = (record.offset + 1,record.topic, record.partition)
        try:
            self.cur.execute(sql, sql_params)
        except Exception as e:
            raise e

    def commit_db_transaction(self,):
        try:
            self.conn.commit()
        except:
            self.conn.rollback()

    def run(self,topic):
        self.consumer.subscribe(topics=[topic, ], listener=SaveOffsetOnRebalance(self))  # 订阅主题
        self.consumer.poll(0)

        for topic_partition in self.consumer.assignment():
            #print(topic_partition,self.get_offset_from_db(topic_partition))
            self.consumer.seek(topic_partition, self.get_offset_from_db(topic_partition))

        try:
            while True:
                msg = self.consumer.poll(timeout_ms=5, max_records=None,
                                    update_offsets=True)  # poll()方法 总是返回由生产者写入kafka但还没有被消费者读取过的记录
                for topic_partion in msg.values():
                    for consumer_record in topic_partion:
                        self.process_recode(consumer_record)
                        self.store_recode_in_db(consumer_record)
                        self.store_offset_in_db(consumer_record)
                else:
                        #self.consumer.commit()
                        self.commit_db_transaction()
                time.sleep(2)
        except Exception as e:
            raise e



if __name__ == '__main__':
    # 获取数据库信息


    kafka_cluster = ['192.168.10.181:9092', '192.168.10.182:9092', '192.168.10.183:9092']  # brokers
    topic = 'foobar' # 主题
    group_id = 'mygroup02'


    consumer = MyKafkaConsumer(kafka_cluster,group_id=group_id)
    consumer.run(topic=topic)






