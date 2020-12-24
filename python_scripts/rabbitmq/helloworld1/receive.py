# -*- coding: utf-8 -*-
# Copyright 2018 WOCHU.CN All Rights Reserved                      #
# SYSTEM   : WochuServerCenter                                       
# FILENAME : @File : worker.py
# FUNCTION : 
# Author: YuZhiYi
# @Time : 2018/10/15 11:44
'''
You may wish to see what queues RabbitMQ has and how many messages are in them. You can do it (as a privileged user) using the rabbitmqctl tool:
sudo rabbitmqctl list_queues
rabbitmqctl.bat list_queues
'''
import pika
credentials = pika.PlainCredentials('wochu','wochu123')
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.14.33',5672,'/',credentials))
channel = connection.channel()
channel.queue_declare(queue = 'hello')

def callback(cb,method,properties,body):
    print(" [x] Recived %r" % body )

channel.basic_consume(callback,queue='hello',no_ack=True)
print(' [*] Wating for messages. To exit press CTRL + C')
channel.start_consuming()
