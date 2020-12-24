# -*- coding: utf-8 -*-
# Copyright 2018 WOCHU.CN All Rights Reserved                      #
# SYSTEM   : WochuServerCenter                                       
# FILENAME : @File : emit_logs_topic.py
# FUNCTION : 
# Author: YuZhiYi
# @Time : 2018/10/15 11:34
#https://pika.readthedocs.io/en/latest/modules/parameters.html
#http://www.rabbitmq.com/tutorials/tutorial-one-python.html
import sys
import random
import pika
#python emit_logs_topic.py 2  message...   有几个点 任务延迟几秒  多个worker 轮询完成任务
credentials = pika.PlainCredentials('wochu','wochu123')
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.14.33',5672,'/',credentials))
channel = connection.channel()
channel.queue_declare(queue = 'task_queue',durable=True)  # durable宣告队列是持久的
message = "Hello World" + ''.join( ['.'for i in range(1,random.randint(2,30))])
channel.basic_publish(exchange='',routing_key='task_queue',body=message,properties=pika.BasicProperties(delivery_mode=2))  # delivery_mode = 2, # 另消息也是持久的
print("[x] Sent" + message)
connection.close()