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
import uuid
import pika
#python emit_logs_topic.py 2  message...   有几个点 任务延迟几秒  多个worker 轮询完成任务
credentials = pika.PlainCredentials('wochu','wochu123')
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.14.33',5672,'/',credentials))
channel = connection.channel()
channel.exchange_declare(exchange='logs',exchange_type='fanout')  # 声明一个名字叫logs的exchange fanout类型 广播
'''Listing exchanges
To list the exchanges on the server you can run the ever useful rabbitmqctl:

sudo rabbitmqctl list_exchanges'''
message = ''.join(sys.argv[1:]) or "Hello World"
channel.basic_publish(exchange='logs',routing_key='',body=message)  # 使用刚刚定义的fanout exchange
'''
Listing bindings
You can list existing bindings using, you guessed it,

rabbitmqctl list_bindings
'''
print("[x] Sent 'Hello World'")
connection.close()