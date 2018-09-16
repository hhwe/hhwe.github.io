**问题**: 任务堆积在broker, 每次重启celery就会从队列中取一个任务, 之后又阻塞在
会出现消息阻塞住: 初步分析可能是消息阻塞了, celery和broker通道由于数据太多而阻塞
**现象**: 重启celery会从队列取一个任务但是马上就阻塞, 重启RabbitMQ后才正常, 猜测应该是大量数据堆积在broker导致RabbitMQ阻塞
**解决**: 在传输的时候数据是经过broker到达worker的, 尽量保持数据轻量. 特别是使用signal任务流形式. 我们使用result_backend保存要传输到下级任务的数据在redis中, 将key传给下级任务就可以了
查看了下RabbitMQ吞吐量大概在20k/s左右, 我开了8个celery线程, 每个产生了大概4k的数据需要通过broker, 导致RabbitMQ阻塞
**总结**: 在任务队列中所有传输数据尽量小

## Redis机器的内网带宽跑满
系统使用单机Redis来做Broker，当连接到Redis的Worker增加的时候，内网流量也迅速增加，最后达到1G，把千兆网卡跑满了，生产者和消费者的性能马上降了下来。通过查看Redis的操作记录，发现大量的发布订阅操作，消息是json格式，除了对传入任务参数的封装，还有Celery本身附带的一些信息，Redis不停地把这些消息发布给各个Worker，而Redis性能真的好，于是产生了每秒1G的流量。 查看了Celery的文档，发现
``` python
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_MESSAGE_COMPRESSION = 'gzip'
```
把json改成Python内置的pickle，并压缩，可以减少一点点消息的大小，但还是跑满了。想到单机的消息队列可能会成为系统的瓶颈，于是把单机Broker改成集群，但是Redis集群用在这里不太好用，看了看RabbitMQ，本身支持集群，镜像模式还可以做HA，性能也可以，果断把Broker改成RabbitMQ集群。拿了两台机器（16G内存）来组成集群，使用HAProxy来做负载均衡，Celery配置加上
``` python
CELERY_QUEUE_HA_POLICY = 'all'
```
然后单机内网流量降了下来，单机峰值在500M/s,但是运行几个小时之后，问题又来了。

## RabbitMQ集群内存爆了
RabbitMQ集群出现OOM了，一番搜索之后RabbitMQ自带的监控插件有可能会占用大量的内存，不看web界面的时候，把插件关闭。
```
rabbitmq-plugins disable rabbitmq_management
```
celery默认会发送服务器的心跳信息，这些我是不需要的，可以通过zabbix等监控，关闭发送，可以在celery启动命令中加上 --without-heartbeat
celery默认会发送大量的任务处理状态事件，这些事件默认是不设置过期时间的，由RabbitMQ的过期时间来处理，所以会有大量的事件数据在RabbitMQ中堆积但又不会被消费。可以在celery配置中加上过期时间，如设置过期时间5s
CELERY_EVENT_QUEUE_TTL = 5
做完这几步之后，RabbitMQ单机内存占用稳定在1~2G，而且内网流量也大幅降了下来，峰值100M/s。

## RabbitMQ流控机制
这个系统生产消息有明显的高峰和低谷，观察高峰时生产者的日志，发现当生产者刚启动时，队列还没有消息的时候，消息入队很快，大概2k/s，然后几十秒之后，发现消息入队越来越慢，入队2k逐渐需要4s、8s、10s。一番搜索之后，发现RabbitMQ有流量控制机制，当生产者过快，消费者来不及消费消息，消息在队列中堆积，RabbitMQ就会阻塞发布消息过快的连击，也就表现为入队逐渐变慢。这时需要注意调整生产和消费的速率，注意RabbitMQ内存占用和内存阀值配置，以及磁盘空间。

其他一些问题
不启用RabbitMQ的confirm机制
RabbitMQ处理confirm消息占用了大量cpu资源。confrim的作用在于当消息真正落地写到磁盘时，给生产者发送ack确认，若生产者在收到该ack后才丢弃该消息，就可以保证消息一定不丢，这是一种非常高强度的可靠性保证。但若没有这么高的要求则可以不启用confirm机制，增加RabbitMQ的吞吐量。

慎用CELERY_ACKS_LATE
Celery的CELERY_ACKS_LATE=True，表示Worker在任务执行完后才向Broker发送acks，告诉队列这个任务已经处理了，而不是在接收任务后执行前发送，这样可以在Worker处理任务过程中异常退出，这个任务还会被发送给别的Worker处理。但是可能的情况是，一个任务会被多次执行，所以一定要慎用。

Celery 任务分队列
耗时和不耗时的任务分开，避免耗时任务阻塞队列；重要和不重要的任务分开，避免重要的任务得不到及时处理。

让Celery忽略处理结果
多数情况下并不需要关注Celery处理的结果，何况在Worker里面我们会记录其结果，设置CELERY_IGNORE_RESULT = True可以让Celery不要把结果发送到Broker，也可以降低内网流量和Broker内存占用。

Celery内存泄露
长时间运行Celery有可能发生内存泄露，可以配置CELERYD_MAX_TASKS_PER_CHILD，让Worker在执行n个任务杀掉子进程再启动新的子进程，可以防止内存泄露。另外Worker执行大量任务后有僵死的情况，启动了一个crontab定时重启Worker。

ip_conntrack: table full, dropping packet
系统执行时会建立大量的连接，造成iptables跟踪表满了，socket拒绝连接，性能提不上去。解决方法：加大 ip_conntrack_max 值。

Inodes满了无法写文件
由于建立了太多的临时文件，发现磁盘没有满，但还是无法写入文件，因为Inodes被用完了，启动一个crontab定时清理临时文件。

