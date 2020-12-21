这个示例为将kafka的topic内的 partition 和 offset 在一个事务中记录到数据库内
这样确保数据既不会被重复写和遗漏

需要系统环境变量里写入数据库信息，本例环境变量为DB_OPS
{"HOST": "xxx.xxx.xxx.xxx", "PORT": xxxx, "USER": "xxxx", "PASSWORD": "xxxxx", "NAME": "xxxx"}

# 记录offset的表
CREATE TABLE `kafka_consumer_offset` (
  `ktopic` varchar(255) DEFAULT NULL,
  `kpartition` int(11) DEFAULT NULL,
  `poffset` int(11) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4

# 记录msg的表
CREATE TABLE `kafka_msg` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ktopic` varchar(255) DEFAULT NULL,
  `kpartition` int(11) DEFAULT NULL,
  `poffset` int(11) DEFAULT NULL,
  `mkey` varchar(255) DEFAULT NULL,
  `mvalue` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
