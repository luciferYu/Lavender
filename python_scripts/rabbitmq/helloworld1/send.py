# -*- coding: utf-8 -*-
# Copyright 2018 WOCHU.CN All Rights Reserved                      #
# SYSTEM   : WochuServerCenter                                       
# FILENAME : @File : emit_logs_topic.py
# FUNCTION : 
# Author: YuZhiYi
# @Time : 2018/10/15 11:34
#https://pika.readthedocs.io/en/latest/modules/parameters.html
#http://www.rabbitmq.com/tutorials/tutorial-one-python.html
import uuid
import pika
credentials = pika.PlainCredentials('wochu','wochu123')
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.14.33',5672,'/',credentials))
channel = connection.channel()
channel.queue_declare(queue = 'hello')
channel.basic_publish(exchange='',routing_key='hello',body='Hello World!' + str(uuid.uuid1()))
print("[x] Sent 'Hello World'")
connection.close()