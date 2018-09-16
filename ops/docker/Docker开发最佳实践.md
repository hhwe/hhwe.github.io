# [Docker development best practices](https://docs.docker.com/develop/dev-best-practices/)

   
预计阅读时间： 6分钟

事实证明，以下开发模式对于使用Docker构建应用程序的人很有帮助。如果您发现了我们应该添加的内容，请 [告诉我们](https://github.com/docker/docker.github.io/issues/new)。

## 如何保持镜像小

在启动容器或服务时，小镜像可以更快地通过网络，并且可以更快地加载到内存中。有一些经验法则可以保持镜像尺寸小：

*   从适当的基本镜像开始。例如，如果您需要JDK，请考虑将您的镜像基于官方`openjdk`镜像，而不是从通用`ubuntu`镜像开始并`openjdk`作为Dockerfile的一部分进行安装
*   [使用多级构建](https://docs.docker.com/engine/userguide/eng-image/multistage-build/)。例如，您可以使用该`maven`镜像构建Java应用程序，然后重置为`tomcat`镜像并将Java工件复制到正确的位置以部署您的应用程序，所有这些都在同一个Dockerfile中。这意味着您的最终镜像不包含构建所引入的所有库和依赖项，而只包含运行它们所需的工件和环境
    *   如果您需要使用不包含多级构建的Docker版本，请尝试通过最小化`RUN`Dockerfile 中单独命令的数量来减少镜像中的图层数。您可以通过将多个命令合并为`RUN`一行并使用shell的机制将它们组合在一起来实现此目的。考虑以下两个片段。第一个在镜像中创建两个图层，而第二个图层仅创建一个图层

        ```
        RUN apt-get -y update
        RUN apt-get install -y python
        ```
        ```
        RUN apt-get -y update && apt-get install -y python
        ```

*   如果您有多个共同点的镜像，请考虑使用共享组件创建自己的 [基本镜像](https://docs.docker.com/engine/userguide/eng-image/baseimages/)，并在其上创建独特的镜像。Docker只需要加载公共层一次，然后缓存它们。这意味着您的衍生镜像可以更有效地使用Docker主机上的内存并加载更快
*   要使生产镜像保持精简但允许调试，请考虑使用生产镜像作为调试镜像的基本镜像。可以在生产镜像之上添加其他测试或调试工具。
*   在构建镜像时，始终使用有用的标记对其进行标记，这些标记用于编码版本信息，预期目标（`prod`或者`test`，例如），稳定性或在不同环境中部署应用程序时有用的其他信息。不要依赖自动创建的`latest`标签。

## 在何处以及如何保留应用程序数据

*   **避免**使用[存储驱动程序](https://docs.docker.com/engine/userguide/storagedriver/)将应用程序数据存储在容器的可写层中 。这会增加容器的大小，从I / O角度来看，与使用卷或绑定装载相比效率较低
*   而是使用[卷](https://docs.docker.com/engine/admin/volumes/volumes/)存储数据
*   适合使用[绑定装入的](https://docs.docker.com/engine/admin/volumes/bind-mounts/)一种情况 是在开发期间，您可能希望将源目录或刚刚构建的二进制文件挂载到容器中。对于生产，请使用卷，将其安装到与开发期间装入绑定装置相同的位置
*   对于生产，使用[机密](https://docs.docker.com/engine/swarm/secrets/)来存储服务使用的敏感应用程序数据，并对 配置文件等非敏感数据使用[配置](https://docs.docker.com/engine/swarm/configs/)。如果您当前使用独立容器，请考虑迁移以使用单一副本服务，以便您可以利用这些仅限服务的功能

## 尽可能使用swarm服务

*   如果可能，请设计您的应用程序，使其能够使用群集服务进行扩展
*   即使您只需要运行应用程序的单个实例，群集服务也可以提供优于独立容器的几个优势。服务的配置是声明性的，Docker始终致力于使所需状态和实际状态保持同步
*   网络和卷可以与群集服务连接和断开连接，Docker处理以无中断方式重新部署各个服务容器。需要手动停止，删除和重新创建独立容器以适应配置更改
*   一些功能，例如存储 [机密](https://docs.docker.com/engine/swarm/secrets/)和[配置的功能](https://docs.docker.com/engine/swarm/configs/)，仅适用于服务而非独立容器。这些功能允许您保持镜像尽可能通用，并避免将敏感数据存储在Docker镜像或容器本身中
*   让我们`docker stack deploy`处理任何镜像，而不是使用 `docker pull`。这样，您的部署不会尝试从已关闭的节点中提取。此外，当新节点添加到群组中时，会自动提取镜像

在群组服务的节点之间共享数据存在限制。如果您使用[Docker for AWS](https://docs.docker.com/docker-for-aws/persistent-data-volumes/)或 [Docker for Azure](https://docs.docker.com/develop/docker-for-azure/persistent-data-volumes/)，您可以使用Cloudstor插件在您的swarm服务节点之间共享数据。您还可以将应用程序数据写入支持同时更新的单独数据库中。

## 使用CI / CD进行测试和部署

*   当您检查对源代码管理的更改或创建拉取请求时，请使用 [Docker Cloud](https://docs.docker.com/docker-cloud/builds/automated-build/)或其他CI / CD管道自动构建和标记Docker镜像并对其进行测试。Docker Cloud还可以将经过测试的应用直接部署到生产环境中

*   通过要求您的开发，测试和安全团队在将镜像部署到生产环境之前对其进行签名，可以进一步了解[Docker EE](https://docs.docker.com/ee/)。这样，您可以确保在将镜像部署到生产环境之前，它已经过测试并由开发，质量和安全团队签署。

## 开发和生产环境的差异

| 发展 | 生产 |
| --- | --- |
| 使用bind mounts为您的容器提供对源代码的访问权限。 | 使用卷来存储容器数据。 |
| 使用Docker for Mac或Docker for Windows。 | 如果可能，请使用Docker EE，并使用[用户映射](https://docs.docker.com/engine/security/userns-remap/)以更好地隔离Docker进程与主机进程。 |
| 不要担心时间漂移。 | 始终在Docker主机上和每个容器进程内运行NTP客户端，并将它们全部同步到同一个NTP服务器。如果使用swarm服务，还要确保每个Docker节点将其时钟与容器同步到同一时间源。 |

[应用](https://docs.docker.com/glossary/?term=application)，[发展](https://docs.docker.com/glossary/?term=development)
