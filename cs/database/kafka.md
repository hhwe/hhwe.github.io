# Kafka介绍

<!-- TOC -->

- [Kafka介绍](#kafka介绍)
        - [ApacheKafka®是*一个分布式流媒体平台*。这到底是什么意思呢？](#apachekafka®是一个分布式流媒体平台这到底是什么意思呢)
            - [[Topics and Logs](https://kafka.apache.org/intro#intro_topics)](#topics-and-logshttpskafkaapacheorgintrointro_topics)
            - [[Distribution](https://kafka.apache.org/intro#intro_distribution)](#distributionhttpskafkaapacheorgintrointro_distribution)
            - [[Geo-replication](https://kafka.apache.org/intro#intro_geo-replication)](#geo-replicationhttpskafkaapacheorgintrointro_geo-replication)
            - [[Producers](https://kafka.apache.org/intro#intro_producers)](#producershttpskafkaapacheorgintrointro_producers)
            - [[Consumers](https://kafka.apache.org/intro#intro_consumers)](#consumershttpskafkaapacheorgintrointro_consumers)
            - [[Multi-tenancy](https://kafka.apache.org/intro#intro_multi-tenancy)](#multi-tenancyhttpskafkaapacheorgintrointro_multi-tenancy)
            - [[Guarantees](https://kafka.apache.org/intro#intro_guarantees)](#guaranteeshttpskafkaapacheorgintrointro_guarantees)
        - [[卡夫卡作为消息系统](https://kafka.apache.org/intro#kafka_mq)](#卡夫卡作为消息系统httpskafkaapacheorgintrokafka_mq)
        - [卡夫卡作为存储系统](#卡夫卡作为存储系统)
        - [Kafka用于流处理](#kafka用于流处理)
        - [把碎片放在一起](#把碎片放在一起)

<!-- /TOC -->

### ApacheKafka®是*一个分布式流媒体平台*。这到底是什么意思呢？

流媒体平台有三个关键功能：

*   发布和订阅记录流，类似于消息队列或企业消息传递系统。
*   以容错的持久方式存储记录流。
*   记录发生时处理流。

Kafka通常用于两大类应用：

*   构建可在系统或应用程序之间可靠获取数据的实时流数据管道
*   构建转换或响应数据流的实时流应用程序

要了解Kafka如何做这些事情，让我们深入探讨Kafka的能力。

首先是几个概念：

*   Kafka作为一个集群运行在一个或多个可跨多个数据中心的服务器上。
*   Kafka集群以称为`topics`类别存储记录流。
*   每条记录都包含一个键(key)，一个值(value)和一个时间戳(timestrap)。

Kafka有四个核心API：

*   [Pruducer API](https://kafka.apache.org/documentation.html#producerapi)允许应用程序发布的记录流至一个或多个kafka的`topics`。
*   [Consumer API](https://kafka.apache.org/documentation.html#consumerapi)允许应用程序订阅一个或多个`topics`，并处理所产生的对他们记录的数据流。
*   [Streams API](https://kafka.apache.org/documentation/streams)允许应用程序充当*流处理器*，从一个或多个主题中消耗的一个输入流，并产生一个输出流至一个或多个输出的主题，有效地变换输入流到输出流。
*   [Connector API](https://kafka.apache.org/documentation.html#connect)允许构建和运行kafka主题连接到现有的应用程序或数据系统中重用生产者或消费者。例如，关系数据库的连接器可能捕获对表的每个更改。

![image](http://upload-images.jianshu.io/upload_images/13148580-5ad87b43216d6e3c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

在Kafka中，客户端和服务器之间的通信是通过简单，高性能，语言无关的[TCP协议完成的](https://kafka.apache.org/protocol.html)。此协议已版本化并保持与旧版本的向后兼容性。我们为Kafka提供Java客户端，但客户端有[多种语言版本](https://cwiki.apache.org/confluence/display/KAFKA/Clients)。

#### [Topics and Logs](https://kafka.apache.org/intro#intro_topics)

让我们首先深入探讨Kafka为记录流提供的核心抽象 - 主题(topics)。

主题是发布记录的类别或订阅源名称。Kafka的主题总是多用户; 也就是说，一个主题可以有零个，一个或多个消费者订阅写入它的数据。

对于每个主题，Kafka群集都维护一个如下所示的分区日志：

![image](http://upload-images.jianshu.io/upload_images/13148580-7136eb4ce6c8de2e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

每个分区都是一个有序的，不可变的记录序列，不断附加到结构化的提交日志中。分区中的记录每个都分配了一个称为*偏移*的顺序ID号，它唯一地标识分区中的每个记录。

Kafka集群持久保存所有已发布的记录 - 无论是否已使用 - 使用可配置的保留期。例如，如果保留策略设置为两天，则在发布记录后的两天内，它可供使用，之后将被丢弃以释放空间。Kafka的性能在数据大小方面实际上是恒定的，因此长时间存储数据不是问题。

![image](http://upload-images.jianshu.io/upload_images/13148580-e2f23a250bd97465.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

实际上，基于每个消费者保留的唯一元数据是该消费者在日志中的偏移或位置。这种偏移由消费者控制：通常消费者在读取记录时会线性地提高其偏移量，但事实上，由于该位置由消费者控制，因此它可以按照自己喜欢的任何顺序消费记录。例如，消费者可以重置为较旧的偏移量来重新处理过去的数据，或者跳到最近的记录并从“现在”开始消费。

这些功能组合意味着Kafka消费者非常便宜 - 他们可以来来往往对集群或其他消费者没有太大影响。例如，您可以使用我们的命令行工具`tail`任何主题的内容，而无需更改任何现有使用者所消耗的内容。

日志中的分区(partitions)有多种用途。首先，它们允许日志扩展到超出适合单个服务器的大小。每个单独的分区必须适合托管它的服务器，但主题可能有许多分区，因此它可以处理任意数量的数据。其次，它们充当了并行性的单位 - 更多的是它。

#### [Distribution](https://kafka.apache.org/intro#intro_distribution)

日志的分区分布在Kafka集群中的服务器上，每个服务器处理数据并请求分区的共享。每个分区都在可配置数量的服务器上进行复制，以实现容错。

每个分区都有一个服务器充当“领导者(leader)”，零个或多个服务器充当“追随者(follower)”。领导者处理分区的所有读取和写入请求，而关注者被动地复制领导者。如果领导者失败，其中一个粉丝将自动成为新的领导者。每个服务器都充当其某些分区的领导者和其他服务器的追随者，因此负载在群集中得到很好的平衡。

#### [Geo-replication](https://kafka.apache.org/intro#intro_geo-replication)

Kafka MirrorMaker为您的群集提供地理复制支持。使用MirrorMaker，可以跨多个数据中心或云区域复制邮件。您可以在主动/被动方案中使用它进行备份和恢复; 或者在主动/主动方案中，将数据放置在离用户较近的位置，或支持数据位置要求。

#### [Producers](https://kafka.apache.org/intro#intro_producers)

生产者将数据发布到他们选择的主题。生产者负责选择分配给主题中哪个分区的记录。这可以以循环方式完成，仅仅是为了平衡负载，或者可以根据一些语义分区功能（例如基于记录中的某些键）来完成。更多关于在一秒钟内使用分区的信息！

#### [Consumers](https://kafka.apache.org/intro#intro_consumers)

消费者使用*消费者组*名称标记自己，并且发布到主题的每个记录被传递到每个订阅消费者组中的一个消费者实例。消费者实例可以在单独的进程中，也可以在不同的机器

如果所有使用者实例具有相同的使用者组，则记录将有效地在使用者实例上进行负载平衡。

如果所有消费者实例具有不同的消费者组，则每个记录将广播到所有消费者进程。

![image](http://upload-images.jianshu.io/upload_images/13148580-45885739f3f798af.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

两个服务器Kafka群集，托管四个分区（P0-P3），包含两个使用者组。消费者组A有两个消费者实例，B组有四个消费者实例。

然而，更常见的是，我们发现主题具有少量的消费者群体，每个“逻辑订户”一个。每个组由许多用于可伸缩性和容错的消费者实例组成。这只不过是发布 - 订阅语义，其中订阅者是消费者群集而不是单个进程。

在Kafka中实现消费的方式是通过在消费者实例上划分日志中的分区，以便每个实例在任何时间点都是分配的“公平份额”的独占消费者。维护组中成员资格的过程由Kafka协议动态处理。如果新实例加入该组，他们将从该组的其他成员接管一些分区; 如果实例死亡，其分区将分发给其余实例。

Kafka仅提供分*区内*记录的总订单，而不是主题中不同分区之间的记录。对于大多数应用程序而言，按分区排序与按键分区数据的能力相结合就足够了。但是，如果您需要对记录进行总订单，则可以使用仅包含一个分区的主题来实现，但这意味着每个使用者组只有一个使用者进程。

#### [Multi-tenancy](https://kafka.apache.org/intro#intro_multi-tenancy)

您可以将Kafka部署为多租户解决方案。通过配置哪些主题可以生成或使用数据来启用多租户。配额也有运营支持。管理员可以定义和强制执行配额，以控制客户端使用的代理资源。有关更多信息，请参阅[安全性文档](https://kafka.apache.org/documentation/#security)。

#### [Guarantees](https://kafka.apache.org/intro#intro_guarantees)

在高级别Kafka提供以下保证：

*   生产者发送到特定主题分区的消息将按其发送顺序附加。也就是说，如果记录M1由与记录M2相同的生产者发送，并且首先发送M1，则M1将具有比M2更低的偏移并且在日志中更早出现。
*   消费者实例按照它们存储在日志中的顺序查看记录。
*   对于具有复制因子N的主题，我们将容忍最多N-1个服务器故障，而不会丢失任何提交到日志的记录。

有关这些保证的更多详细信息，请参见文档的设计部分。

### [卡夫卡作为消息系统](https://kafka.apache.org/intro#kafka_mq)

Kafka的流概念与传统的企业级消息系统相比如何？

消息传统上有两种模型：[queue](http://en.wikipedia.org/wiki/Message_queue)和[publish-subscribe](http://en.wikipedia.org/wiki/Publish%E2%80%93subscribe_pattern)。在队列中，消费者池可以从服务器读取并且每个记录转到其中一个; 在发布 - 订阅中，记录被广播给所有消费者。这两种模型中的每一种都有优点和缺点。排队的优势在于它允许您在多个消费者实例上划分数据处理，从而可以扩展您的处理。不幸的是，一旦一个进程读取它已经消失的数据，队列就不是​​多用户。发布 - 订阅允许您将数据广播到多个进程，但由于每条消息都发送给每个订阅者，因此无法进行扩展处理。

卡夫卡的消费者群体概念概括了这两个概念。与队列一样，使用者组允许您将处理划分为一组进程（使用者组的成员）。与发布 - 订阅一样，Kafka允许您向多个消费者组广播消息。

Kafka模型的优势在于每个主题都具有这些属性 - 它可以扩展处理并且也是多用户 -- 不需要选择其中一个。

与传统的消息系统相比，Kafka具有更强的订购保证。

传统队列在服务器上按顺序保留记录，如果多个消费者从队列中消耗，则服务器按照存储顺序分发记录。但是，虽然服务器按顺序分发记录，但是记录是异步传递给消费者的，因此它们可能会在不同的消费者处出现故障。这实际上意味着在存在并行消耗的情况下丢失记录的顺序。消息传递系统通常通过具有“独占消费者”概念来解决这个问题，该概念只允许一个进程从队列中消耗，但当然这意味着处理中没有并行性。

卡夫卡做得更好。通过在主题中具有并行性概念 - 分区 - ，Kafka能够在消费者流程池中提供订购保证和负载平衡。这是通过将主题中的分区分配给使用者组中的使用者来实现的，以便每个分区仅由该组中的一个使用者使用。通过这样做，我们确保使用者是该分区的唯一读者并按顺序使用数据。由于有许多分区，这仍然可以平衡许多消费者实例的负载。但请注意，消费者组中的消费者实例不能超过分区。

### 卡夫卡作为存储系统

任何允许发布与消费消息分离的消息的消息队列实际上充当了正在进行的消息的存储系统。Kafka的不同之处在于它是一个非常好的存储系统。

写入Kafka的数据将写入磁盘并进行复制以实现容错。Kafka允许生产者等待确认，以便在完全复制之前写入不被认为是完整的，并且即使写入的服务器失败也保证写入仍然存在。

磁盘结构Kafka很好地使用了规模 - 无论服务器上有50KB还是50TB的持久数据，Kafka都会执行相同的操作。

由于认真对待存储并允许客户端控制其读取位置，您可以将Kafka视为一种专用于高性能，低延迟提交日志存储，复制和传播的专用分布式文件系统。

有关Kafka的提交日志存储和复制设计的详细信息，请阅读[此](https://kafka.apache.org/documentation/#design)页面。

### Kafka用于流处理

仅仅读取，写入和存储数据流是不够的，目的是实现流的实时处理。

在Kafka中，流处理器是指从输入主题获取连续数据流，对此输入执行某些处理以及生成连续数据流以输出主题的任何内容。

例如，零售应用程序可能会接收销售和发货的输入流，并输出重新排序流和根据此数据计算的价格调整。

可以使用生产者和消费者API直接进行简单处理。但是，对于更复杂的转换，Kafka提供了完全集成的[Streams API](https://kafka.apache.org/documentation/streams)。这允许构建执行非平凡处理的应用程序，这些应用程序可以计算流的聚合或将流连接在一起。

此工具有助于解决此类应用程序面临的难题：处理无序数据，在代码更改时重新处理输入，执行有状态计算等。

流API构建在Kafka提供的核心原语上：它使用生产者和消费者API进行输入，使用Kafka进行有状态存储，并在流处理器实例之间使用相同的组机制来实现容错。

### 把碎片放在一起

消息传递，存储和流处理的这种组合可能看起来很不寻常，但它对于Kafka作为流媒体平台的作用至关重要。

像HDFS这样的分布式文件系统允许存储静态文件以进行批处理。有效地，这样的系统允许存储和处理过去的*历史*数据。

传统的企业消息系统允许处理您订阅后到达的未来消息。以这种方式构建的应用程序在到达时处理未来数据。

Kafka结合了这两种功能，这种组合对于Kafka作为流媒体应用程序平台以及流数据管道的使用至关重要。

通过组合存储和低延迟订阅，流应用程序可以以相同的方式处理过去和未来的数据。也就是说，单个应用程序可以处理历史存储的数据，而不是在它到达最后一条记录时结束，它可以在未来数据到达时继续处理。这是包含批处理以及消息驱动应用程序的流处理的一般概念。

同样，对于流数据流水线，订阅实时事件的组合使得可以将Kafka用于极低延迟的流水线; 但是，能够可靠地存储数据使得可以将其用于必须保证数据传输的关键数据，或者与仅定期加载数据或可能长时间停机以进行维护的离线系统集成。流处理设施可以在数据到达时对其进行转换。

有关Kafka提供的保证，API和功能的更多信息，请参阅其余[文档](https://kafka.apache.org/documentation.html)。
