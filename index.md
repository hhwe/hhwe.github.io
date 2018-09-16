# Summary

## 目录

* [基础知识](cs/README.md)
    * [计算机网络](cs/network/README.md)
        * [HTTP 协议](cs/network/HTTP.md)
        * [TCP 协议](cs/network/TCP.md)
        * [UDP 协议](cs/network/UDP.md)
        * [IP 协议](cs/network/IP.md)
        * [Socket 编程](cs/network/Socket-Programming-Basic.md)
    * [数据结构与算法](cs/algorithm/README.md)
        * [链表](cs/algorithm/Linked-List.md)
        * [树](cs/algorithm/Tree.md)
        * [哈希表](cs/algorithm/Hash-Table.md)
        * [排序](cs/algorithm/Sorting.md)
        * [搜索]()
        * [字符串]()
        * [向量/矩阵]()
        * [随机](cs/algorithm/Random.md)
        * [贪心](cs/algorithm/Greedy.md)
        * [动态规划](cs/algorithm/DP.md)
    * [体系结构与操作系统](cs/arch/README.md)
        * [体系结构基础](cs/arch/Arch.md)
        * [操作系统基础](cs/arch/OS.md)
        * [并发技术](cs/arch/Concurrency.md)
        * [内存管理](cs/arch/Memory-Management.md)
        * [磁盘与文件](cs/arch/Disk-And-File.md)
    * [数据库系统](cs/database/README.md)
        * [事务处理](cs/database/Transaction.md)
        * [索引](cs/database/DB-Index.md)
    * [编译原理](cs/compiler/README.md)
        * [编译器架构](cs/compiler/Compiler-Arch.md)
    * [设计模式](cs/design/README.md)
        * [面向对象基础](cs/design/OO-Basic.md)
        * [四人帮设计模式](cs/design/GOP.md)
        * [MVC 与 MVVM](cs/design/MVC.md)
    * [版本控制](cs/scm/README.md)
    	* [Git](cs/scm/Git.md)
    	* [SVN](cs/scm/SVN.md)

* [开发](dev/README.md)
    * [python](dev/python/README.md)
        * [15个python面试要点](dev/python/15个python面试要点.md)
        * [Python编码](dev/python/Python编码.md)
        * [Python面试](dev/python/Python面试.md)
        * [requests源码解读](dev/python/requests源码解读.md)
        * [subprocess碰到的各种问题](dev/python/subprocess碰到的各种问题.md)
        * [Celery压力测试](dev/docker/Celery压力测试.md)
        * [Celery文档总结(一)](dev/docker/Celery文档总结(一).md)
        * [Celery文档总结(二)](dev/docker/Celery文档总结(三).md)
        * [Celery文档总结(三)](dev/docker/Celery文档总结(二).md)
        * [Celery测试和调优](dev/docker/Celery测试和调优.md)
        * [Python-Web应用部署](dev/docker/Python-Web应用部署.md)
    * [golang](dev/golang/README.md)
        * [Build-a-web-application-in-Go](dev/golang/Build-a-web-application-in-Go.md)
        * [defer-panic-recover](dev/golang/defer-panic-recover.md)
        * [Golang2错误处理](dev/golang/Golang2错误处理.md)
        * [Go-maps-in-action](dev/golang/Go-maps-in-action.md)
        * [Package-Container](dev/golang/Package-Container.md)

* [运维](ops/README.md)
    * [docker](ops/docker/README.md)
        * [docker](ops/docker/docker.md)
        * [Docker开发最佳实践](ops/docker/Docker开发最佳实践.md)
        * [Docker概述](ops/docker/Docker概述.md)
    * [面试问题](ops/Questions.md)

## 结构:

```
.
├── bug
│   └── 2018-08-13.md
├── cs
│   ├── algorithm
│   │   ├── binary_tree.py
│   │   ├── sort.go
│   │   └── sort.py
│   ├── database
│   │   ├── MongoDB.md
│   │   ├── MySQL事务.md
│   │   ├── RabbitMQ.md
│   │   ├── Redis.md
│   │   ├── 存储过程,函数,触发器.md
│   │   ├── 数据库相关问题.md
│   │   └── 数据库设计.md
│   └── os
│       ├── Linux命令.md
│       ├── Linux进程管理.md
│       ├── Nginx指南.md
│       ├── Shell脚本.md
│       └── 各种软件命令.md
├── dev
│   ├── golang
│   │   ├── Build-a-web-application-in-Go.md
│   │   ├── defer-panic-recover.md
│   │   ├── Golang2错误处理.md
│   │   ├── Go-maps-in-action.md
│   │   └── Package-Container.md
│   ├── javascript
│   │   └── 2018-08-02.md
│   └── python
│       ├── 15个python面试要点.md
│       ├── Celery压力测试.md
│       ├── Celery文档总结(一).md
│       ├── Celery文档总结(三).md
│       ├── Celery文档总结(二).md
│       ├── Celery测试和调优.md
│       ├── Python-Web应用部署.md
│       ├── Python编码.md
│       ├── Python面试.md
│       ├── requests源码解读.md
│       └── subprocess碰到的各种问题.md
├── index.md
├── LICENSE
├── ops
│   └── docker
│       ├── docker.md
│       ├── Docker开发最佳实践.md
│       ├── Docker概述.md
│       ├── images
│       │   ├── Dockerfile参考.md
│       │   ├── 使用多阶段构建.md
│       │   ├── 创建基本镜像.md
│       │   └── 编写Dockerfiles的最佳实践.md
│       └── kubernetes
│           ├── Dockerfile
│           └── server.js
├── README.md
├── static
└── web
    ├── Web基础.md
    ├── web攻击.md
    └── 跨域.md
```
