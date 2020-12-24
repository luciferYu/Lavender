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
import time

credentials = pika.PlainCredentials('wochu','wochu123')
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.14.33',5672,'/',credentials))
channel = connection.channel()
channel.queue_declare(queue='task_queue',durable=True) # durable宣告队列是持久的

def callback(ch,method,properties,body):
    print(" [x] Recived %r" % body )
    time.sleep(body.count(b'.'))
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)
    '''
    Forgotten acknowledgment
    It's a common mistake to miss the basic_ack. It's an easy error, but the consequences are serious. Messages will be redelivered when your client quits (which may look like random redelivery), but RabbitMQ will eat more and more memory as it won't be able to release any unacked messages.

    In order to debug this kind of mistake you can use rabbitmqctl to print the messages_unacknowledged field:
    sudo rabbitmqctl list_queues name messages_ready messages_unacknowledged
    
    On Windows, drop the sudo:
    rabbitmqctl.bat list_queues name messages_ready messages_unacknowledged
    '''

channel.basic_consume(callback,queue='task_queue')  # 在新版本中 此处参数位置发生了变化 channel.basic_consume('task_queue',callback)
channel.basic_qos(prefetch_count=1)
print(' [*] Wating for messages. To exit press CTRL + C')
channel.start_consuming()



