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

credentials = pika.PlainCredentials('wochu', 'wochu123')
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.14.33', 5672, '/', credentials))
channel = connection.channel()
channel.exchange_declare(exchange='direct_logs', exchange_type='direct')  # 声明一个名字叫direct_logs的exchange 类型是direct
'''
We will use a direct exchange instead. 
The routing algorithm behind a direct exchange is simple - a message goes to the queues whose binding key exactly matches the routing key of the message.
'''
result = channel.queue_declare(exclusive=True)  # 声明一个随机名字的队列，并且当退出时删除队列（exclusive=True）
queue_name = result.method.queue
for serverity in ['info','warning']:
    channel.queue_bind(exchange='direct_logs', queue=queue_name, routing_key=serverity)  # 订阅 info 和 warning的信息


def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key,body))


channel.basic_consume(callback, queue=queue_name, no_ack=True)
print(' [*] Wating for messages. To exit press CTRL + C')
channel.start_consuming()
