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
import random
import time
credentials = pika.PlainCredentials('wochu','wochu123')
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.14.33',5672,'/',credentials))
channel = connection.channel()
channel.exchange_declare(exchange='direct_logs',exchange_type='direct')  # 使用direct 类型
for i in range(1000): #随机发布100条
    message = ''.join(sys.argv[1:]) or str(uuid.uuid1())
    serverity = random.choice(['info','error','warning']) # 随机选择一个 routingkey
    channel.basic_publish(exchange='direct_logs',routing_key=serverity,body=message)
    time.sleep(0.1)
    print("[x] Sent %r %r" % (serverity, message))

connection.close()