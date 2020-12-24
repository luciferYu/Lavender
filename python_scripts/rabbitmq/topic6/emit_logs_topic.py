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
import pika
'''
And to emit a log with a routing key "kern.critical" type:
python emit_log_topic.py "kern.critical" "A critical kernel error"
'''


credentials = pika.PlainCredentials('wochu','wochu123')
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.14.33',5672,'/',credentials))
channel = connection.channel()
channel.exchange_declare(exchange='topic_logs',exchange_type='topic')  # 使用topic 类型
routing_key = sys.argv[1] if len(sys.argv) > 2 else 'anonymous.info'
message = ' '.join(sys.argv[2:]) or 'Hello World!'
channel.basic_publish(exchange='topic_logs',
                      routing_key=routing_key,
                      body=message)
print(" [x] Sent %r:%r" % (routing_key, message))
connection.close()