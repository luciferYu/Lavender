# -*- coding: utf-8 -*-
# Copyright 2018 WOCHU.CN All Rights Reserved                      #
# SYSTEM   : WochuServerCenter                                       
# FILENAME : @File : receive_logs_topic.py
# FUNCTION : 
# Author: YuZhiYi
# @Time : 2018/10/15 11:44
'''
You may wish to see what queues RabbitMQ has and how many messages are in them. You can do it (as a privileged user) using the rabbitmqctl tool:
sudo rabbitmqctl list_queues
rabbitmqctl.bat list_queues
'''
import pika
import time
import sys
'''
To receive all the logs run:

python receive_logs_topic.py "#"
To receive all logs from the facility "kern":

python receive_logs_topic.py "kern.*"
Or if you want to hear only about "critical" logs:

python receive_logs_topic.py "*.critical"
You can create multiple bindings:

python receive_logs_topic.py "kern.*" "*.critical"
And to emit a log with a routing key "kern.critical" type:

python emit_log_topic.py "kern.critical" "A critical kernel error"
'''


credentials = pika.PlainCredentials('wochu', 'wochu123')
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.14.33', 5672, '/', credentials))
channel = connection.channel()
channel.exchange_declare(exchange='topic_logs', exchange_type='topic')  # 声明一个名字叫direct_logs的exchange 类型是direct
result = channel.queue_declare(exclusive=True)  # 声明一个随机名字的队列，并且当退出时删除队列（exclusive=True）
queue_name = result.method.queue


binding_keys = sys.argv[1:]
if not binding_keys:
    sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
    sys.exit(1)

for binding_key in binding_keys:
    channel.queue_bind(exchange='topic_logs',
                       queue=queue_name,
                       routing_key=binding_key)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()
