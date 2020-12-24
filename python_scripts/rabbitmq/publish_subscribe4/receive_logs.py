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

credentials = pika.PlainCredentials('wochu','wochu123')
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.14.33',5672,'/',credentials))
channel = connection.channel()
channel.exchange_declare(exchange='logs',exchange_type='fanout')  # 声明一个名字叫logs的exchange fanout类型 广播
result = channel.queue_declare(exclusive=True)  # 声明一个随机名字的队列，并且当退出时删除队列（exclusive=True）
queue_name = result.method.queue
channel.queue_bind(exchange='logs',queue=queue_name) # 将新建的随机名称队列与exchange进行绑定


def callback(ch,method,properties,body):
    print(" [x] %r" % body )

channel.basic_consume(callback,queue=queue_name,no_ack=True)
print(' [*] Wating for messages. To exit press CTRL + C')
channel.start_consuming()
