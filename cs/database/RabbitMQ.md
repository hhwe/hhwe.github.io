## Ubuntu上安装配置RabbitMQ

```
sudo apt instlal rabbitmq-server
rabbitmq-plugins enable rabbitmq_management  # 打开web界面
rabbitmqctl list_queues  # 列出所有队列
```
rabbitmq默认guest用户如果外网无法访问web, 需要修改rabbitmq.config文件中的loopback_users设为空: 
```
[{rabbit, [{loopback_users, []}]}].
```

## RabbitMQ和Kafka区别

RabbitMQ被设计为通用消息代理，采用点对点，请求/回复和pub-sub通信样式模式的多种变体。它使用智能代理/哑消费者模型，专注于向消费者提供一致的消息传递，消费者的消费速度与经纪人跟踪消费者状态的速度大致相似。它是成熟的，在正确配置时表现良好，得到很好的支持（客户端库Java，.NET，node.js，Ruby，PHP和更多语言），并且有许多可用的插件可以将它扩展到更多的用例和集成场景。

![rabbitmq broker.png](https://upload-images.jianshu.io/upload_images/13148580-4dca5af32f3da02d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

RabbitMQ中的通信可以根据需要同步或异步。发布者向交换发送消息，消费者从队列中检索消息。通过交换将生产者与队列分离可确保生产者不会受到硬编码路由决策的影响。RabbitMQ还提供了许多分布式部署方案（并且确实要求所有节点都能够解析主机名）。可以将多节点群集设置为群集联合，并且不依赖于外部服务（但某些群集形成插件可以使用AWS API，DNS，Consul等）。  

Apache Kafka专为高容量发布 - 订阅消息和流而设计，旨在持久，快速和可扩展。从本质上讲，Kafka提供了一个持久的消息存储，类似于日志，在服务器集群中运行，它存储称为主题的类别中的记录流。

![apache kafka.png](https://upload-images.jianshu.io/upload_images/13148580-8617ae5b9d33bc46.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


