# 一些kafka的运维命令
/data/kafka/bin/kafka-console-consumer.sh --bootstrap-server 192.168.10.181:9092 --topic foobar --from-beginning
/data/kafka/bin/kafka-topics.sh --list --zookeeper --zookeeper  192.168.10.181:2181,192.168.10.182:2181,192.168.10.183:2181
/data/kafka/bin/kafka-topics.sh --create  --zookeeper  192.168.10.181:2181,192.168.10.182:2181,192.168.10.183:2181 --replication-factor 2 --partitions 16 --topic foobar
/data/kafka/bin/kafka-topics.sh --zookeeper  192.168.10.181:2181,192.168.10.182:2181,192.168.10.183:2181 --delete --topic foobar
/data/kafka/bin/kafka-topics.sh --describe  --zookeeper  192.168.10.181:2181,192.168.10.182:2181,192.168.10.183:2181 --topic foobar
/data/kafka/bin/kafka-configs.sh --describe --zookeeper  192.168.10.181:2181,192.168.10.182:2181,192.168.10.183:2181 --entity-type topics
 echo status | nc localhost 2181

[root@bigdata01 ~]# /data/kafka/bin/kafka-console-producer.sh --broker-list localhost:9092 --topic test
>hello world01
>hello word02
Ctrl + d

[root@bigdata01 ~]# /data/kafka/bin/kafka-console-consumer.sh --zookeeper localhost:2181 --topic test --from-beginning
Using the ConsoleConsumer with old consumer is deprecated and will be removed in a future major release. Consider using the new consumer by passing [bootstrap-server] instead of [zookeeper].
hello world01
hello word02
ctrl + c
