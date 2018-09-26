# Redis Sentinel

<!-- TOC -->

- [Redis Sentinel](#redis-sentinel)
    - [概述](#概述)
    - [快速入门](#快速入门)
        - [获得哨兵](#获得哨兵)
        - [运行哨兵](#运行哨兵)
        - [部署哨兵之前需要了解的基本事情](#部署哨兵之前需要了解的基本事情)
        - [配置哨兵](#配置哨兵)
        - [Sentinel部署示例](#sentinel部署示例)
    - [快速教程](#快速教程)
        - [访问Sentinel master的状态](#访问sentinel-master的状态)
        - [获取当前master地址](#获取当前master地址)
        - [测试故障转移](#测试故障转移)
    - [Sentinel API](#sentinel-api)
        - [Sentinel 命令](#sentinel-命令)
        - [运行时配置Sentinel](#运行时配置sentinel)
        - [添加或删除Sentinel](#添加或删除sentinel)
        - [删除老master或不可及的slave](#删除老master或不可及的slave)
        - [发布/订阅消息](#发布订阅消息)
        - [处理 -BUSY状态](#处理--busy状态)
        - [Slaves优先级](#slaves优先级)
        - [Sentinel和Redis身份验证](#sentinel和redis身份验证)
        - [Sentinel客户端实现](#sentinel客户端实现)
    - [更多高级概念](#更多高级概念)
        - [SDOWN和ODOWN故障状态](#sdown和odown故障状态)
        - [自动发现Sentinels和Slaves](#自动发现sentinels和slaves)
        - [故障转移过程之外的重新配置](#故障转移过程之外的重新配置)
        - [Slave选择和优先级](#slave选择和优先级)
    - [算法和内部构建](#算法和内部构建)
        - [Quorum](#quorum)
        - [配置 epochs](#配置-epochs)
        - [配置传播](#配置传播)
        - [分区下的一致性](#分区下的一致性)
        - [Sentinel持久化状态](#sentinel持久化状态)
        - [TILT 模式](#tilt-模式)

<!-- /TOC -->

## 概述

Redis哨兵为Redis提供了高可用性。实际上这意味着你可以使用哨兵模式创建一个可以不用人为干预而应对各种故障的Redis部署。

哨兵模式还提供了其他的附加功能，如监控，通知，为客户端提供配置。

下面是在宏观层面上哨兵模式的功能列表：

+ 监控：哨兵不断的检查master和slave是否正常的运行。
+ 通知：当监控的某台Redis实例发生问题时，可以通过API通知系统管理员和其他的应用程序。
+ 自动故障转移：如果一个master不正常运行了，哨兵可以启动一个故障转移进程，将一个slave升级成为master，其他的slave被重新配置使用新的master，并且应用程序使用Redis服务端通知的新地址。
+ 配置提供者：哨兵作为Redis客户端发现的权威来源：客户端连接到哨兵请求当前可靠的master的地址。如果发生故障，哨兵将报告新地址。

哨兵的分布式特性, Redis哨兵是一个分布式系统：

哨兵自身被设计成和多个哨兵进程一起合作运行。有多个哨兵进程合作的好处有：

+ 当多个哨兵对一个master不再可用达成一致时执行故障检测。这会降低错误判断的概率。
+ 即使在不是所有的哨兵都工作时哨兵也会工作，使系统健壮的抵抗故障。毕竟在故障系统里单点故障没有什么意义。

Redis的哨兵、Redis实例(master和slave)、和客户端是一个有特种功能的大型分布式系统。在这个文档里将逐步从为了理解哨兵基本性质需要的基础信息，到为了理解怎样正确的使用哨兵工作的更复杂的信息(这是可选的)进行介绍。

## 快速入门

### 获得哨兵

当前的哨兵版本是`sentinel 2`。它是基于最初哨兵的实现，使用更健壮的和更简单的预算算法(在这个文档里有解释)重写的。Redis2.8和Redis3.0附带稳定的哨兵版本。他们是Redis的两个最新稳定版本。在不稳定版本的分支上执行新的改进，且有时一些新特性一旦被认为是稳定的就会被移植到Redis2.8和Redis3.0分支中。Redis2.6附带Redis sentinel 1，它是弃用的不建议使用。

### 运行哨兵

如果你使用可执行的 `redis-sentinel`(或者你有可执行的redis-server)，你可以使用下面的命令行运行哨兵：

```sh
redis-sentinel /path/to/sentinel.conf
```

另外你可以直接使用可执行的redis-server在哨兵模式下启动。

```sh
redis-server /path/to/sentinel.conf --sentinel
```

两种方式效果都是一样的。

然而在启动哨兵时必须使用一个配置文件，因为这个配置文件将用于系统保存当前状态和在重启时重新加载。哨兵会在没有指定配置文件或指定的配置文件不可写的时候拒绝启动。

Redis 哨兵默认监听26379 TCP端口，所以为了哨兵的正常工作，你的26379端口必须开放接收其他哨兵实例的IP地址的连接。否则哨兵不能通信和商定做什么，故障转移将永不会执行。

### 部署哨兵之前需要了解的基本事情

+ 一个健壮的部署至少需要三个哨兵实例。
+ 三个哨兵实例应该放置在客户使用独立方式确认故障的计算机或虚拟机中。例如不同的物理机或不同可用区域的虚拟机。
+ sentinel + Redis实例不保证在故障期间保留确认的写入，因为Redis使用异步复制。然而有方式部署哨兵使丢失数据限制在特定时刻，虽然有更安全的方式部署它。
+ 你的客户端要支持哨兵，流行的客户端都支持哨兵，但不是全部。
+ 没有HA设置是安全的，如果你不经常的在开发环境测试，在生产环境他们会更好。你可能会有一个明显的错误配置只是当太晚的时候。
+ Sentinel，Docker，或者其他形式的网络地址交换或端口映射需要加倍小心：Docker执行端口重新映射，破坏Sentinel自动发现其他的哨兵进程和master的slave列表。稍后在这个文档里检查关于Sentinel和Docker的部分，了解更多信息。

### 配置哨兵

Redis源码发布包包含一个sentinel.conf的文件，它是一个自含的配置文件示例，你可以使用它配置哨兵，一个典型的最小的配置文件就像下面的配置：

```conf
sentinel monitor mymaster 127.0.0.1 6379 2
sentinel down-after-milliseconds mymaster 60000
sentinel failover-timeout mymaster 180000
sentinel parallel-syncs mymaster 1

sentinel monitor resque 192.168.1.3 6380 4
sentinel down-after-milliseconds resque 10000
sentinel failover-timeout resque 180000
sentinel parallel-syncs resque 5
```

你只需要指定masters监控，给予每个分开的master不同的名字。不需要指定slaves，它们是自动发现的。Sentinel会自动的更新关于slaves的附加信息(为了保留信息以防重启)。每次slave晋升为一个master或者每次发现新的Sentinel都会重写配置。

上面的示例配置中，主要监控两组Redis示例，每个由一个master和若干个slave组成。一组实例叫mymaster，另一组叫 resque。

sentinel monitor的参数声明的含义如下所示：

```sh
sentinel monitor [master-group-name] [ip] [port] [quorum]
```

为了更清晰，我们逐行的解释每个选项的含义：

第一行用于告诉Redis监控一个master叫做mymaster，它的地址在127.0.0.1，端口为6379，法定人数是2。每个参数都很容易理解，但是quorum需要解释一下：

+ quorum是Sentinel需要协商同意master是否可到达的数量。为了真正的标记slave为失败，并最终是否需要启动一个故障转移进程。
+ 无论怎样，quorum只用于检测故障。为了实际执行故障转移，Sentinel需要选举leader并进行授权。这只发生在大多数Sentinel进程的选举。

例如你有5个哨兵进程，并且给定的master的quorum的值设置为2，这是将发生的事情：

+ 如果两个哨兵进程同时同意master是不可到达的，这两个哨兵的其中一个将启动一个故障转移。
+ 如果至少三个哨兵可获得，故障转移将会被授权并真实的启动。

实际上这意味着在故障转移期间如果大多数的Sentinel进程不能通信，Sentinel将会永不启动故障转移(即在少数分区没有故障转移)。

其他的选项通常是这种形式：

```sh
sentinel [option_name] [master_name] [option_value]
```

并且用于下面的目的：

+ down-after-milliseconds - 一个实例不可到达(不能ping通或者有错误)，Sentinel开始认为它是down的毫秒数。
+ parallel-syncs - 设置在故障转移之后同时可以重新配置使用新master的slave的数量。数字越低，更多的时间将会用故障转移完成，但是如果slaves配置为服务旧数据，你可能不希望所有的slave同时重新同步master。因为主从复制对于slave是非阻塞的，当停止从master加载批量数据时有一个片刻延迟。通过设置选项为1，确信每次只有一个slave是不可到达的。

其他的选项在本文档其他部分有描述，并且在示例sentinel.conf的备有文件里有附带说明。

所有的Sentinel参数在运行时可以使用SENTINEL SET命令更改。查看在运行时重新配置Sentinel部分了解更多。

### Sentinel部署示例

既然你知道了sentinel的基本信息，你可以很想知道应该将Sentinel放置在哪里，需要多少Sentinel进程等等。这个章节展示了几个部署示例。

我们为了图像化展示配置示例使用字符艺术，这是不同符号的意思：

```sh
+--------------------+
| This is a computer |
| or VM that fails   |
| independently. We  |
| call it a "box"    |
+--------------------+
```

我们写在盒子里表示他们正在运行什么：

```sh
+-------------------+
| Redis master M1   |
| Redis Sentinel S1 |
+-------------------+
```

不同的盒子之间通过线条连接，表示他们可以相互通信：

```sh
+-------------+               +-------------+
| Sentinel S1 |---------------| Sentinel S2 |
+-------------+               +-------------+
```

使用斜杠展示网络断开：

```sh
+-------------+                +-------------+
| Sentinel S1 |------ // ------| Sentinel S2 |
+-------------+                +-------------+
```

还要注意：

+ Master 被叫做 M1,M2,M3 ... Mn。
+ Slave 被叫做 R1,R2,R3 ... Rn(replica的首字母)
+ Sentinels 被叫做 S1,S2,S3 ... Sn
+ Clients 被叫做 C1,C2,C3 ... Cn
+ 当一个实例因为Sentinel的行为改变了角色，我们把它放在方括号里，所以[M1]表示因为Sentinel的介入，M1现在是一个master。

**注意**永远不会显示的设置只是使用了两个哨兵，因为为了启动故障转移，Sentinel总是需要和其他大多数的Sentinel通信。

`实例1，只有两个Sentinel，不要这样做`

```sh
+----+         +----+
| M1 |---------| R1 |
| S1 |         | S2 |
+----+         +----+

Configuration: quorum = 1
```

+ 在这个设置中，如果master M1故障，R1将被晋升因为两个Sentinel可以达成协议并且还可以授权一个故障转移因为多数就是两个。所以他表面上看起来是可以工作的，然而检查下一个点了解为什么这个设置是不行的。
+ 如果运行M1的盒子停止工作了，S1也停止工作。运行在其他盒子上的S2将不能授权故障转移，所以系统将变成不可用。

**注意**为了排列不同的故障转移需要少数服从多数，并且稍后向所有的Sentinel传播最新的配置。还要注意上面配置的故障转移的能力，没有任何协定，非常危险：

```sh
+----+           +------+
| M1 |----//-----| [M1] |
| S1 |           | S2   |
+----+           +------+
```

在上面的配置中我们使用完美的对称方式创建了两个master(假定S2可以在未授权的情况下进行故障转移)。客户端可能会不确定往哪边写，并且没有途径知道什么时候分区配置是正确的，为了预防一个永久的断裂状态。

所有请永远部署至少三个Sentinel在三个不同的盒子里。

`例2：使用三个盒子的基本设置`

这是个非常简单的设置，它有简单调整安全的优势。它基于三个盒子，每个盒子同时运行一个Redis实例和一个Sentinel实例。

```sh
       +----+
       | M1 |
       | S1 |
       +----+
          |
+----+    |    +----+
| R2 |----+----| R3 |
| S2 |         | S3 |
+----+         +----+

Configuration: quorum = 2
```

如果M1故障，S2和S3将会商定故障并授权故障转移，使客户端可以继续。

在每个Sentinel设置里，Redis是异步主从复制，总会有丢失数据的风险，因为有可能当它成为master的时候，一个确认的写入操作还没有同步到slave。然后在上面的设置中有一个更高的风险由于客户端分区一直是老的master，就像下面的图像所示：

```sh
         +----+
         | M1 |
         | S1 | [- C1 (writes will be lost)
         +----+
            |
            /
            /
+------+    |    +----+
| [M2] |----+----| R3 |
| S2   |         | S3 |
+------+         +----+
```

在这个案例中网络分区隔离老的master M1，所以slave R2晋升为master。然而客户端，比如C1，还在原来的老的master的分区，可能继续往老master写数据。这个数据将会永久丢失，因为分区恢复时，master将会重新配置为新master的slave，丢弃它的数据集。

这个问题可以使用下面的Redis主从复制特性减轻，它可在master检查到它不再能传输它的写入操作到指定数量的slave的时候停止接收写入操作。

```conf
min-slaves-to-write 1
min-slaves-max-lag 10
```

使用上面的配置(请查看自带的redis.conf示例了解更多信息)一个Redis实例，当作为一个master，如果它不能写入至少1个slave将停止接收写入操作。（N个Slave以上不通就停止接收）

由于主从复制是异步的不能真实的写入，意味着slave断开连接，或者不再向我们发送异步确认的指定的max-lag秒数。（判定连接不通的超时时间）

在上面的示例中使用这个配置，老master M1将会在10秒钟后变为不可用。当分区恢复时，Sentinel配置将指向新的一个，客户端C1将能够获取到有效的配置并且将使用新master继续工作。

然而天下没有免费的午餐，这种改进，如果两个slave挂掉，master将会停止接收写入操作。这是个权衡。

`例三：Sentinel在客户端盒子里`

有时我们只有两个Redis盒子可用，一个master和一个slave。在例二中的配置在那样的情况下是不可行的，所谓我们可以借助下面的，Sentinel放置在客户端：

```sh
            +----+         +----+
            | M1 |----+----| R1 |
            | S1 |    |    | S2 |
            +----+    |    +----+
                      |
         +------------+------------+
         |            |            |
         |            |            |
      +----+        +----+      +----+
      | C1 |        | C2 |      | C3 |
      | S1 |        | S2 |      | S3 |
      +----+        +----+      +----+

      Configuration: quorum = 2
```

在这个设置里，Sentinel的视角和客户端的视角相同：如果大多数的客户端认为master是可以到达的，它就是好的。C1,C2,C3是一般的客户端，这不意味着C1识别单独的客户端连接到Redis。它更像一些如应用服务，Rails应用之类的。

如果运行M1和S1的盒子故障，故障转移将会发生，然而很容看到不同的网络分区将导致不同的行为。例如如果客户端和Redis服务之间的断开连接，Sentinel将不能设置，因为master和slave将都不可用。

注意如果使用M1获取分区，我们有一个和例二中描述的相似的问题，不同的是这里我们没有办法打破对称，由于只有一个slave和master，所以当它的master断开连接时master不能停止接收查询，否则在slave故障期间master将永不可用。

所以这是个有效的设置但是在例二中的设置有像更容易管理HA系统的优点， 并有能力限制master接收写入的时间。

`例4：少于3个客户端的Sentinel客户端`

在例3中如果客户端少于3个就不能使用。在这个案例中我们使用一个混合的设置：

```sh
            +----+         +----+
            | M1 |----+----| R1 |
            | S1 |    |    | S2 |
            +----+    |    +----+
                      |
               +------+-----+
               |            |  
               |            |
            +----+        +----+
            | C1 |        | C2 |
            | S3 |        | S4 |
            +----+        +----+

      Configuration: quorum = 3
```

这里和例3非常类似，但是这里我们在4个盒子里运行四个哨兵。如果M1故障其他的三个哨兵可以执行故障转移。

Sentinel，Docker，NAT，和可能的问题
Docker使用一个叫端口映射的技术：程序运行在Docker容器可以暴露一个不同端口。这非常有助于在相同的服务器上相同的时间使用相同的端口运行多个容器。

Docker不仅仅可以实现这个功能，还有其他的设置可以重新映射端口，有时是端口，有时是IP地址。

重新映射端口和地址有两个问题：

1. Sentinel自动发现其他不再工作的Sentinel，因为它基于每个Sentinel监听连接的端口和IP的问候消息。然而不知道地址和端口是重新映射的，所以它会宣告不正确的配置信息。
2. Slaves以相同的方式列在master的Info输出里：通过master检测每个TCP连接检测地址，因为端口是通过slave自己在握手期间广告的，然而端口就像第一点里说的是错误的。

## 快速教程

本文接下来的章节里，将逐步覆盖关于Sentinel API，配置，和语义的所有细节。然而对于那些想尽快使用系统的人，这个章节是一个教程，展示怎么使用三个Sentinel实例配置。

这里我们假定实例已经运行在5000,5001,5002。还假定Redis master运行在6379端口，slave运行在6380端口。在这个教程里我们使用IPv4回路地址127.0.0.1，假定运行在你的个人电脑里。

三个Sentinel配置文件应该是这样的：

```conf
port 5000
sentinel monitor mymaster 127.0.0.1 6379 2
sentinel down-after-milliseconds mymaster 5000
sentinel failover-timeout mymaster 60000
sentinel parallel-syncs mymaster 1
```

另外的两个配置文件除了使用5001和5002端口外，其他全部相同。

上面的配置中需要注意一些事情：

+ master 叫做 mymaster。它标识master和它的slave。因为每个master设置有个不同的名字，Sentinel可以同时监控不同组的master和slave。
+ quorum设置为2(sentinel monitor指令的最后一个参数)。
+ down-after-milliseconds 的值为5000毫秒，也就是5秒，所以一旦我们在这个时间范围内不能接收响应，master将会被标记为故障。

一旦你启动三个Sentinel，你将会看到一些消息日志，像：

```log
+monitor master mymaster 127.0.0.1 6379 quorum 2
```

这是Sentinel事件，如果你SUBSCRIBE事件名称,你可以通过Pub/Sub接收到各种事件。

Sentinel在故障检测和转移期间生产并记录不同的事件。

### 访问Sentinel master的状态

开始使用Sentinel最明显的事情是，检查master是否正常监控：

```sh
$ redis-cli -p 5000
127.0.0.1:5000] sentinel master mymaster
 1) "name"
 2) "mymaster"
 3) "ip"
 4) "127.0.0.1"
 5) "port"
 6) "6379"
 7) "runid"
 8) "953ae6a589449c13ddefaee3538d356d287f509b"
 9) "flags"
1)  "master"
2)  "link-pending-commands"
3)  "0"
4)  "link-refcount"
5)  "1"
6)  "last-ping-sent"
7)  "0"
8)  "last-ok-ping-reply"
9)  "735"
10) "last-ping-reply"
11) "735"
12) "down-after-milliseconds"
13) "5000"
14) "info-refresh"
15) "126"
16) "role-reported"
17) "master"
18) "role-reported-time"
19) "532439"
20) "config-epoch"
21) "1"
22) "num-slaves"
23) "1"
24) "num-other-sentinels"
25) "2"
26) "quorum"
27) "2"
28) "failover-timeout"
29) "60000"
30) "parallel-syncs"
31) "1"
```

就像你看到的，它打印了大量的关于master的信息。有一些是对于我们非常有用的：

1. num-other-sentinels 是2，所以我们知道Sentinel已经检测到这个master的其他两个Sentinel。如果你检查日志，你会看到生成了 +sentinel 事件。
2. flags 是 master。如果master down了，我们在这里希望看到 s_down 或者 o_down。
3. num-slaves这里是1，所以Sentinel还检测到master有一个slave。

为了更多的探索这个实例，你可能想尝试下面的两个命令：

```sh
SENTINEL slaves mymaster
SENTINEL sentinels mymaster
```

第一个会打印连接到master的slave的信息，第二个是关于其他Sentinel的信息。

### 获取当前master地址

我们已经说明，Sentinel还可以作为客户端的配置提供者，连接到一组master和slave。因为故障转移和重新配置，客户端没有办法指定谁是当前活动master，所以Sentinel提供了一个API解决这个问题：

```sh
127.0.0.1:5000> SENTINEL get-master-addr-by-name mymaster
1) "127.0.0.1"
2) "6379"
```

### 测试故障转移

这时候我们部署的sentinel已经准备好了测试。我们只需要kill掉master检查配置是否改变。所以只需要做如下的事情：

```sh
redis-cli -p 6379 DEBUG sleep 30
```

这个命令将使master休眠30秒不能访问。这主要是模仿master由于一些原因挂掉。

如果你检查Sentinel日志，以应该能看到很多动作：

1. 每个Sentinel检查到master挂掉，有一个+sdown事件。
2. 这个时间稍后升级到 +odown，这意味着多个Sentinel商定了master不可到达的事实。
3. Sentinels投票选举一个Sentinel启动第一次故障转移。
4. 发生故障转移。

如果你再次访问 mymaster 当前master的地址，最终你这次应该得到一个不一样的答案：

```sh
127.0.0.1:5000] SENTINEL get-master-addr-by-name mymaster
1) "127.0.0.1"
2) "6380"
```

到目前位置一切都顺利，这个时候你可以跳转到创建Sentinel部署或者可以阅读更多信息了解所有的Sentinel命令和内部构建。

## Sentinel API

Sentinel 提供了一个AP以便于检查它的状态，检查监控的master和slave的健康，订阅接收特定的通知，和在运行时改变Sentinel配置。

Sentinel默认使用TCP端口26379(注意6379是标准的Redis端口)。Sentinels使用Redis协议接收命令，所以你可以使用 redis-cli 或任何其他的Redis客户端和Sentinel通信。

可以直接查询Sentinel检查监控的Redis实例的状态，查看它知道的其它Sentinel，等等。或者，使用Pub/Sub，可以从Sentinel接收推送类型的通知，每次有事件发生，例如故障转移，或者实例进入错误条件，等等。

### Sentinel 命令

下面是一系列的接收命令，而不是全部的命令，用于修改Sentinel配置。

```sh
PING - 这个命令简单的返回PONE。
SENTINEL masters - 展示监控的master清单和它们的状态。
SENTINEL master [master name] - 展示指定master的状态和信息。
SENTINEL slaves [master name] - 展示master的slave清单和它们的状态。
SENTINEL sentinels [master name] - 展示master的sentinel实例的清单和它们的状态。
SENTINEL get-master-addr-by-name [master name] - 返回master的IP和端口。如果故障转移在处理中或成功终止，返回晋升的slave的IP和端口。
SENTINEL reset [pattern] - 这个命令将重置所有匹配名字的masters。参数是blog风格的。重置的过程清空master的所有状态，并移除已经发现和关联master的所有slave和sentinel。
SENTINEL failover [master name] - 如果master不可到达，强制执行一个故障转移，而不征求其他Sentinel的同意。
SENTINEL ckquorum [master name] - 检查当前的Sentinel配置是否能够到达故障转移需要的法定人数，并且需要授权故障转移的多数。这个命令应该用于监控系统检查部署是否正确。
SENTINEL flushconfig - 强制Sentinel在磁盘上重写它的配置，包括当前的Sentinel状态。通常Sentinel每次重写配置改变它的状态。然而有时由于操作错误、硬盘故障、包升级脚本或配置管理器可能导致配置文件丢失。在这种情况下收到强制Sentinel重写配置文件。这个命令即使上面的配置文件完全不见了。
```

### 运行时配置Sentinel

从Redis 2.8.4开始，Sentinel提供了API以便于添加、删除、或者修改指定master的配置。注意如果有多个Sentinel，应该申请更改所有的Redis Sentinel实例。这意味这修改一台Sentinel不会在网络上自动传播到其他的Sentinel实例。

下面是SENTINEL的子命令清单，用于修改Sentinel实例的配置。

```sh
SENTINEL MONITOR  [name] [ip] [port] [quorum] - 这个命令告诉Sentinal开始使用指定的name、ip、port、quorum监控新master。这个sentinel.conf配置文件里的指令完全相同，区别是这里不能使用主机名作为IP，你需要提供一个IPv4或IPv6地址。
SENTINEL REMOVE  [name] - 用于删除指定的master：master将不再受监控，并从Sentinel内部状态完全删除，所以通过SENTINEL masters命令不会再列处理，等等。
SENTINEL SET [name] [option] [value] - SET命令和Redis的CONFIG SET 非常相似，用于修改指定master的配置参数。可以指定多组option / value。所有通过sentinel.conf配置的参数都可以通过SET命令设置。
```

下面是一个SENTINEL SET 命令的例子，用于修改名叫objects-cache的master的down-after-milliseconds。

```sh
SENTINEL SET objects-cache-master down-after-milliseconds 1000
```

正如前面提到的，SENTINEL SET 可以用于配置所有可在启动配置文件里设置的参数。此外还可以值更改quorum配置而不用删除和重新添加master，只是使用：

```sh
SENTINEL SET objects-cache-master quorum 5
```

**注意**没有对应的GET命令因为SENTINEL MASTER以简单的格式提供了所有的配置参数。

### 添加或删除Sentinel

添加新的Sentinel非常简单因为Sentinel实现了自动检测的机制。你需要做的就是启动新的Sentinel配置监控当前活动的master。10秒之内Sentinel就会获得其他的Sentinel列表和master的slave。

如果你需要一次添加多个Sentinel，建议添加一个之后再添加另一个，在添加下一个之前等待其他的Sentinel已经知道了第一个Sentinel。这有助于始终保证可以在一个分区获得多数，在添加Sentinel过程中发生故障的机会。

通过每添加一个Sentinel有一个30秒的延迟非常容易获得。在这个过程的最后要使用命令`SENTINEL MASTER mastername`一边检查是否所有Sentinel同意监控master的Sentinel的总数。

删除Sentinel有点复杂：Sentinel永远不会忘记见到过的Sentinel，即使它们在很长时间内不能到达，因为我们不希望动态的改变需要授权的多数并创建一个新值。所以为了删除一个Sentinel应该在网络分区里执行以下步骤：

1. 停止想要删除的Sentinel进程。
2. 发送一个`SENTINEL RESET *` 命令到所有的Sentinel实例。在执行实例之间每个至少等待30秒钟。
3. 检查所有Sentinel协商的当前活动的Sentinel数量，通过检查每个Sentinel的`SENTINEL MASTER mastername`输出。

### 删除老master或不可及的slave

Sentinels从不会忘记指定master的slave，即使他们有很长时间不可及。这非常有用，因为Sentinels应该能够正确的重新配置网络分区或故障事件之后返回的slave。

此外，故障转移之后，转移故障的master实质上添加作为新master的slave，这个方式一旦它再次可用就会重新配置从新master复制。

然而有时候你可能想从哨兵监控的slave列表里永久的删除一个salve(也可能是老master)。

为了做到这个事情，你需要向所有的哨兵发送一个`SENTINEL RESET mastername`命令：他们将会在10秒内刷新slave列表，只添加一个列表复制当前master的信息输出。

### 发布/订阅消息

客户端可以使用Sentinel作为Redis兼容的发布/订阅服务器以便于SUBSCRIBE或PSUBSCRIBE通道并获得关于特殊事件的通知。

通道的名字和事件的名字相同。比如通道的名字是 +sdown 将会接收所有实例进入 SDOWN 状态的通知。(SDWON意思是实例从Sentinel的视角不再可及)

订阅所有的消息只需要使用 `PSUBSCRIBE *`。

下面是你可以使用的API通道和消息格式列表。第一个单词是通道/事件名称,其余的部分是数据格式。

**注意：**指定的 instance details部分意思是提供下面的参数确定目标实例。

```sh
[instance-type] [name] [ip] [port] @ [master-name] [master-ip] [master-port]

# 表示master的部分(从@到最后)是可选的并只在实例不是master自己的时候指定。
+reset-master [instance details] -- master被重置。
+slave [instance details] -- 发现附加一个新slave。
+failover-state-reconf-slave [instance  details] -- 故障转移状态更改为 reconf-slaves 状态。
+failover-detected [instance details] -- 有另一个Sentinel启动一个故障转移或者任何其他的外部实体被检测到(附加的salve变成master)。
+slave-reconf-sent [instance details] -- leader sentinel向实体发送 SALVEOF命令以便于重新配置新Slave。
+slave-reconf-inprog [instance details] -- slave正在被从新配置为新master的slave，但是同步过程还没有完成。
+slave-reconf-done [instance details] -- slave现在已经同步到新master。
-dup-sentinel [instance details] -- 指定master的一个或多个Sentinel被移除。(当Sentinel实例重启时会发生)
+sentinel [instance details] -- 发现添加一个sentinel。
+sdown [instance details] -- 指定的实例现在在主观上是Down状态。
-sdown [instance details] -- 指定的实例不再是主观上的Down状态。
+odown [instance details] -- 指定的实例现在在客观上是Down状态。
-odown [instance details] -- 指定的实例在客观上不再是Down状态。
+new-epoch [instance details] -- 当前时代被更新。
+try-failover [instance details] -- 新故障转移过程中，等待其他多数决定。
+elected-leader [instance details] -- 指定的时代赢得了选举，可以执行故障转移。
+failover-state-select-slave [instance details] -- 新的故障转移状态是 select-slave：尝试查找适当晋升的slave。
no-good-slave [instance details] -- 没有适当晋升的slave。稍后重试，但是这可能会发生改变并终止故障转移。
selected-slave [instance details] -- 找到适合晋升的slave。
failover-state-send-slaveof-noone [instance details] -- 尝试重新配置晋升的slave作为master，等待转换。
failover-end-for-timeout [instance details] -- 由于超时终止故障转移，不管怎样,slave最后将被配置为复制新master。
failover-end [instance details] -- 故障转移成功完成。所有slaves被重新配置为新master的从。
switch-master [master name] [oldip] [oldport] [newip] [newport] -- 在改变配置之后指定master新IP和地址。这是大多数外部用户感兴趣的消息。
+tilt -- 进入 Tilt模式。
-tilt -- 退出 Tilt模式
```

### 处理 -BUSY状态

当Lua脚本运行时间超过配置的Lua脚本时间限制时，Redis实例返回-BUSY错误。在触发故障转移之前发生这种情况时，Sentinel将尝试发送一个 `SCRIPT KILL`命令，它只在脚本只读的时候成功。

如果尝试过这个之后实例仍是一个错误状态，最后就会启动故障转移。

### Slaves优先级

Redis实例有一个salve-priority的配置参数。这个信息暴露在Redis slave的 INFO 输出里，Sentinel使用它以便于在可用的salves中获取slave进行故障转移：

1. 如果Slave优先级设置为0.slave永远不会晋升为master。
2. 优先级数字越低越被Sentinel优先选择。

例如如果有一个slave S1在当前master的同一个数据中心，并且另一个salve S2在另一个数据中心，可以设置S1的优先级为10，S2的优先级为100，所以如果master故障并且S1和S2都可用，S1将会被优先选择。

了解关于slave选择的更多信息，请参考 本文档的 slave选择和优先级部分。

### Sentinel和Redis身份验证

当master配置要求从客户端提供密码作为安全措施时，slave也需要知道这个密码以便于master的身份验证并建立master-slave之间的连接用于异步复制协议。

通过以下配置指令可以实现：

+ requirepass 在master里，设置身份验证密码，并确定实例不处理没有身份验证的客户端请求。
+ masterauth 在slave里，为了slave验证master以便于从master正确的复制数据。

当使用Sentinel时，没有单独的master，因为在故障转移之后slave可以改变master的角色，并且老master可以被重新配置为slave，所以你要做的是在master和slaves的所有实例里都配置上上面的指令。

这通常也是一个理智的设置因为你不只是想保护master里的数据，在slave里也是一样。

然而在一些罕见的情况下你需要slave不进行身份验证就可以访问，你可以将slave的优先级设置为0，放置这个slave升级为master，并在这个slave里只配置masterauth指令，不用requirepass指令，以便于没有授权的客户端也可以访问。

### Sentinel客户端实现

Sentinel需要显示的客户端支持，除非系统被配置为执行脚本对所有请求执行重定向到新master实例。客户端类库的实现话题在文档[Sentinel clients guidelines](https://redis.io/topics/sentinel-clients)有覆盖。

## 更多高级概念

接下来的部分我们将会涉及Sentinel怎么工作的一些细节，没有依靠实现细节和算法并会在本文档的其他部分涉及。

### SDOWN和ODOWN故障状态

Redis Sentinel对于正在down的状态有两个不同的概念，一个叫做主管的DOWN(SDOWN)，它是一个本地Sentinel实例的状态。另一个叫客户端的Down(ODOWN)，当足够的Sentinel SDOWN状态是可达的，并且从其他的Sentinel使用`SENTINEL is-master-down-by-addr`命令得到反馈，就进入ODOWN状态。

从Sentinel的视角，当它在配置文件`is-master-down-after-milliseconds`参数指定的时间之内没有收到有效的PING响应就会进入一个SDOWN条件。

PING的响应是下面的其中之一：

+ PONE
+ -LOADING 错误
+ -MASTERDOWN 错误

任何其他的响应都视为无效。但是注意一个合理的master通知自己在INFO输出里作为salve被视为down。

**注意**SDOWN要求不可接受的请求是对整个配置间隔，所以例如如果间隔是30000毫秒，且我们每29秒接受的一个ping请求，实例被认为是正常运行的。

SDOWN不能触发故障转移：这只是意味着一个单独Sentinel认为Redis实例不可及。触发一个故障转移，必须到达ODWN状态。

从SDOWN转换到ODOWN没有共识的算法，仅仅是形式上的：如果一个指定的Sentinel从足够多的Sentinel获得报告在指定的时间范围内master没有工作，SDOWN就升级为ODOWN。如果确认在稍后丢失，标记就被清空。

更严格的身份验证是需要大多数确认以便于真正的启动故障转移，但是没有到ODOWN状态不会触发故障转移。

ODOWN只适用于master。其他的实例Sentinel不要求，所以SLAVE和其他sentinel永远不会到达ODOWN状态，仅仅是SDOWN。

SDOWN还有其他含义。例如Sentinel执行故障转移时slave在SDOWN状态不会被选中晋级。

### 自动发现Sentinels和Slaves

Sentinel保持与其他Sentinel的连接以便于相互的检查可用性，并传输消息。然而你不需要在每个Sentinel实例里配置其他Sentinel的地址，因为Sentinel使用Redis实例的发布/订阅功能用于发现监控相同master和slave的其他Sentinel。

这个功能由向_sentinel_:hello通道发送问候消息实现。

同样你不需要配置master附加的slave列表，因为Sentinel会自动发现。

+ Sentinel每两秒发布一个消息到每个监控的master和slave 发布/订阅通道_sentinel_hello，消息内容包括ip，port，runid宣布他的存在。
+ Sentinel订阅每个master和slave的_sentinel_:hello通道，查找不知道的sentinels。一旦检测到新的sentinel，他们就添加为这个master的sentinel。
+ 问候消息包括当前master完整的配置。如果Sentinel有一个配置比接收的老，它会立刻更新配置。
+ 在添加sentinel到master之前，sentinel总是检测是否已经有相同runid或相同地址的sentinel。在这种情况下会删除所有匹配的sentinel，并添加新的。

### 故障转移过程之外的重新配置

即使不进行故障转移，Sentinel也会一直尝试设置当前配置。特别的：

+ Slaves成为master，将会配置为当前master的slave。
+ Slave连接到错误的master，会重新配置为正确的master。

Sentinels重新配置slaves，有时必须监控错误配置，比周期性的广播新配置要好。

Sentinel使用状态配置信息在接收更新之前尝试改变slaves配置。

还要注意怎样尝试利用当前配置防止故障分区：

+ Master在可用的时候被重新配置为slave。
+ Slaves分区在重新配置分区期间一旦可及就会被重新配置。

在这个部分要记住的重要的是：Sentinel是一个系统，每个进程一直尝试利用最后一个合理的配置设置监控的实例。

### Slave选择和优先级

当Sentinel实例准备执行故障转移时，由于master在ODOWN状态且从多数的Sentinel实例接收到授权，需要选择一个适当的slave。

选择过程会评估slave下面的信息：

1. 从master断开的次数。
2. Slave优先级。
3. 复制偏移量。
4. Run ID。

发现Slave从master断开超过10倍的超时时间，加上Sentinel认为master不可用的时间，就认为不适合故障转移并跳过。

更严格的条件，slave的INFO输出信息显示从master断开超过：

```sh
(down-after-milliseconds * 10) + milliseconds_since_master_is_in_SDOWN_state
```

被认为是不适合的并完全忽略。

Slave选择只认为通过上面的测试，并在上面的标准基础上排序：

1. Slave通过Redis实例的redis.conf文件配置的slave-priority排序。优先级越低越被优先考虑。
2. 如果优先级相同，检查slave的复制偏移量，并选择接收更多数据的slave。
3. 如果多个slave有相同的优先级和同样的处理数据过程，就会执行一个更进一步的验证，选择一个有较短run ID的slave。run ID 对于 slave没太大用，但是非常有助于选择slave的过程，而不是随机选择slave。

如果要强烈的匹配，Redis master和slaves都要配置 salve-priority。否则所有的实例可以使用默认的run ID运行(建议这样设置，因为这比通过复制偏移量选择slave更感兴趣)。

Redis实例可以配置特定的slave-priority为0用于永远不让sentinel选举为master。但是用这种方式配置slave会在故障转移之后重新配置以便于复制新master的数据，不同的只是他永远不会变成一个master。

## 算法和内部构建

在接下来的部分我们将会探究Sentinel特性的细节。用户不需要关注所有的细节，但是深度理解可以帮你更有效的开发和操作Sentinel。

### Quorum

上面的章节中展示了每个监控的master都关联一个quorum配置。它指定需要商定master不可及或错误条件Sentinel进程数量以便于触发故障转移。

然而，触发故障转移之后，为了真正的执行故障转移，至少大多数的Sentinel必须授权Sentinel进行故障转移。如果只有少数的Sentinel存在，Sentinel将永远不会执行故障转移。

让我们试着使事情更清晰：

+ Quorum：需要检测错误条件以便于标记master为ODOWN的Sentinel进程数量。
+ 通过ODOWN状态触发故障转移。
+ 一旦触发了故障转移，Sentinel尝试请求大多数的Sentinel授权故障转移（如果quorun设置的数量大于多数，则需要大于等于）。

不同之处似乎很小，但是很容易理解和使用。例如如果你有5个Sentinel实例，quorum设置为2，一旦2个Sentinel认为master不可及就会触发故障转移，但是只有其中一个Sentinel得到至少3个同意的时候才可以故障转移。

如果把quorum配置为5，所有的Sentinel都必须统一master的错误条件，且从所有的Sentinel得到授权才可以故障转移。

这意味着quorum可以通过两个方式用于调整Sentinel：

1. 如果quorum设置的值小于我们部署的大多数Sentinel，这基本上是合理的，即使少数的Sentinel不可通信业可以触发故障转移。
2. 如果quorum设置的值大于多数的Sentinels，只有当大多数的Sentinel连接正常并同意才可以故障转移。

### 配置 epochs

Sentinel要求从多数获得授权以便于启动故障转移有几个重要原因：

当一个Sentinel被授权，它得到一个唯一的配置epoch控制故障转移。这是一个数字它将用于在故障转移之后新配置的版本。因为多数同意授权指定的版本到指定的Sentinel，没有其他的Sentinel能够使用它。这意味着每个故障转移的配置都有一个唯一的版本。我们就知道了这为什么这么重要。

此外Sentinel有个规则：如果Sentinel选举其他的Sentinel启动指定master的故障转移，它将等待一些时间再次尝试相同的master。这个延迟时间你可以在sentinel.conf文件里配置failover-time。

这意味着Sentinel在相同的时间不会尝试相同的master，先尝试第一个授权，如果失败在段时间后尝试另一个，以此类推。

Redis Sentinel保证liveness属性如果多数Sentinels可以通信，最后就会被授权故障转移如果master是down。

Redis Sentinel还保证safety属性每个Sentinel将使用不同的configuration epoch转移相同的master。

### 配置传播

一旦Sentinel能够成功的故障转移master，它将启动传播新的配置以便于其他的Sentinel更新指定master的信息。

一个故障转移被认为是成功的，它需要Sentinel能够发送`SLAVEOF NO ONE`命令到选择的slave，并且切换到master稍后会在master的INFO输出里观察。

这时候，即使在slave的重新配置过程中，故障转移也被认为是成功的，且所有的Sentinel被要求报告新配置。

新配置方式的传播方式就是为什么我们需要用不同的版本号(epoch)授权每个Sentiel故障转移的原因。

每个Sentinel使用发布/订阅消息的方式连续不断的传播它的配置版本，在相同的时间所有的Sentinel等待消息查看其他Sentinel传播的配置是什么。

配置信息在`_sentinel_:hello`发布/订阅通道里广播。

因为每个配置有不同的版本号，高版本总是胜过低版本。

所以比如所有的Sentinel认为master在192.168.1.53:6379。这个配置的版本是1.一些时间之后被授权的故障转移版本是2.如果故障转移成功，它会开始广播新配置，比如192.168.1.50:9000.所有的其他实例会看到这个版本号是2的配置并更新他们的配置，因为新的配置有更高的版本号。

这意味着Sentinel保证一个第二leveness属性：一组Sentinel能够通信并汇集更高保本号更新相同的配置。

基本上如果网络分区，每个分区将汇集更高的本地配置。在特殊的案例中没有分区，有一个单独的分区且每个Sentinel会商定配置。

### 分区下的一致性

Redis Sentinel配置最终是一致的，所以配个分区将汇集更高可用的配置。然而在现实系统中使用Sentinel有三个不同的角色：

+ Redis Instances。
+ Sentinel instances。
+ Clients。

为了定义系统特性我们必须考虑这三个角色。

下面是一个简单的有三个节点的网络，每个节点运行一个Redis实例和一个Sentinel实例：

```sh
            +-------------+
            | Sentinel 1  |----- Client A
            | Redis 1 (M) |
            +-------------+
                    |
                    |
+-------------+     |          +------------+
| Sentinel 2  |-----+-- // ----| Sentinel 3 |----- Client B
| Redis 2 (S) |                | Redis 3 (M)|
+-------------+                +------------+
```

这个系统中初始状态是Redis3是master，Redis1和2是slaves。发生了一个分区隔离了老master，Sentnel1和2启动一个故障转移将Sentinel 1升级为master。

Sentinel属性保证Sentinel1和2现在有master的新配置。然而3始终是老配置因为它在不同的分区里。

我们知道当网络分区修复之后Sentinel3会获取更新的配置，然而在分区期间如果有客户端连接老master分区会发生什么？

客户端会始终能写到Redis 3，老的master。当分区重新接入，Redis 3将重新变为Redis 1的salve，并且所有在分区期间写入的数据都将会丢失。

根据你的配置你可能不想让这个事情发生：

+ 如果你正在使用Redis作为缓存，它可以使客户端B能够写入到老master，即使数据丢失。
+ 如果你正在作为存储，这就不好了而且你需要配置系统以便于部分的防止这个问题。

因为Redis是异步复制，没有办法完全的防止数据丢失，然而你可以使用下面的配置选项绑定Redis3和Redis1之间的松散度。

```sh
min-slaves-to-write 1
min-slaves-max-lag 10
```

使用上面的配置，当切换master时，如果有1台以上slave不可写入就会停止接收写入操作。

因为主从复制是异步的，slave断开连接或者不发送异步确认大于指定的max-lag的秒数意味着不能真正的写入。

在上面的例子中使用这个配置，Redis3会在10秒之后变为不可用。当分区恢复时，Sentinel 3配置将汇集新的，且Client B能够检查有效的配置并继续。

通常Redis+Sentinel作为一个整体是一个最终一致的系统，且数据丢弃老的复制当前master的数据，所以始终有一个丢失确认写入的窗口。这是因为Redis异步复制。注意这是Sentinel自身的限制，如果你想完整一致的故障转移，相同的属性将仍然适用。有两个方法避免丢失确认的写入：

1. 使用同步复制
2. 使用一致性系统。

Redis现在不能使用上面的任何系统，并且这在开发目标之外。但是有代理实现的方案2，例如SoundCoud Roshi，或者 Netfix Dynomite。

### Sentinel持久化状态

Sentinel状态持久化到Sentinel配置文件里。例如每次接收一个新配置，或者创建，配置文件会和配置epoch一起持久化到硬盘上。

这意味着在停止和重启Sentinel进程的时候是安全的。

### TILT 模式

Redis Sentinel严重依赖于计算机时间：例如为了理解一个实例是否可用，它记录上次成功响应PING命令的时间，并和当前时间对比分析已经多久了。

然而如果计算机时间意外的改变了，或者计算机非常忙，或者进程由于某些原因损坏，Sentinel可能会有一个意想不到的行为。

TILT模式是一个特殊的 "protection" 模式，当检测到可以降低系统可靠性怪异现象时，Sentinel可以进入 "protection" 模式。Sentinel时间计数器一般每秒调用10次，所以我们期望大约100毫秒在两个调用之间中断。

什么哨兵调用中断定时器，并和当前调用对比：如果时常是负数或出乎意料的大(2秒或更大)就进入TILT模式。

当进入TILT模式，Sentinel将继续监控每件事，除了：

+ 停止代理。
+ 开始否定的回答SENTINEL is-master-down-by-addr请求，不再可信。
+ 一切恢复正常30秒之后，就退出TILT模式。

注意在某些方面TILT模式可以使用很多内核支持的单调时钟API替换。然而仍不清楚这是否是一个好的解决方案，因为当前系统避免问题的过程只是在很长时间暂停或不执行调度。
