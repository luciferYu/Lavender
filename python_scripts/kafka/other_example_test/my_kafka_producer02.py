#!/data/exec/python/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/1 11:47
# @Author  : YuZhiYi
# @Email   : yuzhiyi@54.com
import json
import datetime
import time
import random
import uuid
from kafka import KafkaProducer
kafka_cluster = ['192.168.10.181:9092','192.168.10.182:9092','192.168.10.183:9092']
producer = KafkaProducer(bootstrap_servers=kafka_cluster,batch_size=16384)
for _ in range(100):
    msg_dict = {
        "dt": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        #"datetime": datetime.datetime.now().timestamp(),
        "uuid": str(uuid.uuid4()),
        "msg": str(_)
    }
    msg = json.dumps(msg_dict)
    print(msg)
    # send(topic, value=None, key=None, headers=None, partition=None, timestamp_ms=None)
    future = producer.send('test', msg.encode('utf-8') )
    result = future.get(timeout=10)
    print(result)
    time.sleep(random.randint(1,3))
producer.close()
