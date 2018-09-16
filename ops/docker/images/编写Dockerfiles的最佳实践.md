# 编写Dockerfiles的最佳实践

###### [Best practices for writing Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#additional-resources)

预计阅读时间： 26分钟

本文档介绍了构建高效镜像的建议最佳实践和方法。

Docker通过从一个`Dockerfile`包含所有命令的文本文件中读取指令来自动构建镜像 ，这些命令按顺序构建给定镜像。A `Dockerfile`遵循特定的格式和指令集，您可以在[Dockerfile参考中](https://docs.docker.com/engine/reference/builder/)找到[它们](https://docs.docker.com/engine/reference/builder/)。

Docker镜像由只读层组成，每个层都代表一个Dockerfile指令。这些层是堆叠的，每一层都是前一层变化的增量。考虑一下`Dockerfile`：

```docker
FROM ubuntu:15.04
COPY . /app
RUN make /app
CMD python /app/app.py
```

每条指令创建一个层：

*   `FROM`从`ubuntu:15.04`Docker镜像创建一个图层。
*   `COPY`从Docker客户端的当前目录添加文件。
*   `RUN`用你的应用程序构建`make`。
*   `CMD` 指定在容器中运行的命令。

运行镜像并生成容器时，可以 在基础图层的顶部添加新的*可写层*（“容器图层”）。对正在运行的容器所做的所有更改（例如写入新文件，修改现有文件和删除文件）都将写入此可写容器层。

有关镜像图层的更多信息（以及Docker如何构建和存储镜像），请参阅 [关于存储驱动程序](https://docs.docker.com/storage/storagedriver/)。

## 一般准则和建议

### 创建短暂的容器

您定义的镜像`Dockerfile`应该生成尽可能短暂的容器。通过“短暂”，我们的意思是容器可以被停止和销毁，然后重建并用绝对最小的设置和配置替换。

请参阅*十二因素应用程序* 方法下*的*[流程](https://12factor.net/processes)，以了解以无状态方式运行容器的动机。

### 了解构建上下文

发出`docker build`命令时，当前工作目录称为*构建上下文*。默认情况下，假定Dockerfile位于此处，但您可以使用文件flag（`-f`）指定其他位置。无论`Dockerfile`实际存在的位置如何，当前目录中的所有文件和目录的递归内容都将作为构建上下文发送到Docker守护程序。

> 构建上下文示例
> 
> 为构建上下文创建一个目录并`cd`进入该目录。将“hello”写入名为的文本文件，`hello`并创建一个`cat`在其上运行的Dockerfile 。从构建上下文（`.`）中构建镜像：
> 
> ```docker
> mkdir myproject && cd myproject
> echo "hello" > hello
> echo -e "FROM busybox\nCOPY /hello /\nRUN cat /hello" > Dockerfile
> docker build -t helloapp:v1 .
> ```
> 
> 移动`Dockerfile`并`hello`进入单独的目录并构建镜像的第二个版本（不依赖于上一个版本的缓存）。使用`-f` 指向Dockerfile并指定构建上下文的目录：
> 
> ```docker
> mkdir -p dockerfiles context
> mv Dockerfile dockerfiles && mv hello context
> docker build --no-cache -t helloapp:v2 -f dockerfiles/Dockerfile context
> ```

无意中包含构建镜像不需要的文件会导致更大的构建上下文和更大的镜像大小。这可以增加构建镜像的时间，拉取和推送镜像的时间以及容器运行时大小。要查看构建上下文有多大，请在构建以下内容时查找类似这样的消息`Dockerfile`：

```docker
Sending build context to Docker daemon  187.8MB
```

### 通过`stdin`管道Dockerfile

Docker 17.05增加了`Dockerfile`通过 `stdin`使用*本地或远程构建上下文*进行管道来构建镜像的功能。在早期版本中，使用从`stdin`写入`Dockerfile`构建镜像并未发送构建上下文。

**Docker 17.04及更低版本**

```docker
docker build -t foo -<<EOF
FROM busybox
RUN echo "hello world"
EOF
```

**Docker 17.05及更高版本（本地构建上下文）**

```docker
docker build -t foo . -f-<<EOF
FROM busybox
RUN echo "hello world"
COPY . /my-copied-files
EOF
```

**Docker 17.05及更高版本（远程构建上下文）**

```docker
docker build -t foo https://github.com/thajeztah/pgadmin4-docker.git -f-<<EOF
FROM busybox
COPY LICENSE config_local.py /usr/local/lib/python2.7/site-packages/pgadmin4/
EOF
```

### .dockerignore

要排除与构建无关的文件（不重构源存储库），请使用`.dockerignore`文件。此文件支持与`.gitignore`文件类似的排除模式。有关创建一个的信息，请参阅 [.dockerignore文件](https://docs.docker.com/engine/reference/builder/#dockerignore-file)。

### 使用多阶段构建

[多阶段构建](https://docs.docker.com/develop/develop-images/multistage-build/)（在[Docker 17.05](https://docs.docker.com/release-notes/docker-ce/#17050-ce-2017-05-04)或更高版本中）允许您大幅减小最终镜像的大小，而不必费力地减少中间层和文件的数量。

由于镜像是在构建过程的最后阶段构建的，因此可以通过[利用构建缓存](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#leverage-build-cache)来最小化镜像层。

例如，如果您的构建包含多个图层，则可以从较不频繁更改（以确保构建缓存可重用）到更频繁更改的顺序对它们进行排序：

*   安装构建应用程序所需的工具
*   安装或更新库依赖项
*   生成您的应用程序

Go应用程序的Dockerfile可能如下所示：

```docker
FROM golang:1.9.2-alpine3.6 AS build

# Install tools required for project
# Run `docker build --no-cache .` to update dependencies
RUN apk add --no-cache git
RUN go get github.com/golang/dep/cmd/dep

# List project dependencies with Gopkg.toml and Gopkg.lock
# These layers are only re-built when Gopkg files are updated
COPY Gopkg.lock Gopkg.toml /go/src/project/
WORKDIR /go/src/project/
# Install library dependencies
RUN dep ensure -vendor-only

# Copy the entire project and build it
# This layer is rebuilt when a file changes in the project directory
COPY . /go/src/project/
RUN go build -o /bin/project

# This results in a single layer image
FROM scratch
COPY --from=build /bin/project /bin/project
ENTRYPOINT ["/bin/project"]
CMD ["--help"]
```

### 不要安装不必要的包

为了降低复杂性，依赖性，文件大小和构建时间，避免安装额外的或不必要的软件包，因为它们可能“很好”。例如，您不需要在数据库镜像中包含文本编辑器。

### 解耦应用程序

每个容器应该只有一个问题。将应用程序分离到多个容器中可以更容易地水平扩展和重用容器。例如，Web应用程序堆栈可能包含三个独立的容器，每个容器都有自己独特的镜像，以分离的方式管理Web应用程序，数据库和内存缓存。

将每个容器限制为一个进程是一个很好的经验法则，但它并不是一个严格的规则。例如，不仅可以[使用init进程生成](https://docs.docker.com/engine/reference/run/#specify-an-init-process)容器 ，而且某些程序可能会自行生成其他进程。例如，[Celery](http://www.celeryproject.org/)可以生成多个工作进程，[Apache](https://httpd.apache.org/)可以为每个请求创建一个进程。

使用您的最佳判断，尽可能保持容器清洁和模块化。如果容器彼此依赖，则可以使用[Docker容器网络](https://docs.docker.com/engine/userguide/networking/) 来确保这些容器可以进行通信。

### 最小化层数

在旧版本的Docker中，最大限度地减少镜像中的图层数量以确保它们具有高性能非常重要。添加了以下功能以减少此限制：

*   在docker1.10和更高，只有指令`RUN`，`COPY`，`ADD`创建图层。其他指令创建临时中间镜像，而不是直接增加构建的大小
*   在Docker 17.05及更高版本中，您可以执行[多阶段构建，](https://docs.docker.com/develop/develop-images/multistage-build/) 并仅将所需的工件复制到最终镜像中。这允许您在中间构建阶段中包含工具和调试信息，而不会增加最终镜像的大小

### 对多行参数进行排序

只要有可能，通过按字母数字方式对多行参数进行排序，可以缓解以后的更改。这有助于避免重复包并使列表更容易更新。这也使PR更容易阅​​读和审查。在反斜杠（`\`）之前添加空格也有帮助。

下面是来自一个示例[`buildpack-deps`镜像](https://github.com/docker-library/buildpack-deps)：

```docker
RUN apt-get update && apt-get install -y \
  bzr \
  cvs \
  git \
  mercurial \
  subversion
```

### 利用构建缓存

构建镜像时，Docker会逐步`Dockerfile`执行您的指令， 按指定的顺序执行每个指令。在检查每条指令时，Docker会在其缓存中查找可以重用的现有镜像，而不是创建新的（重复）镜像。

如果您根本不想使用缓存，则可以使用命令中的`--no-cache=true` 选项`docker build`。但是，如果你让Docker使用它的缓存，重要的是要了解它何时可以找到匹配的镜像。Docker遵循的基本规则概述如下：

*   从已经在高速缓存中的父镜像开始，将下一条指令与从该基本镜像导出的所有子镜像进行比较，以查看它们中的一个是否使用完全相同的指令构建。如果不是，则缓存无效
*   在大多数情况下，只需将`Dockerfile`其中一个子镜像中的指令进行比较就足够了。但是，某些说明需要更多的检查和解释
*   对于`ADD`和`COPY`指令，检查镜像中文件的内容，并计算每个文件的校验和。在这些校验和中不考虑文件的最后修改时间和最后访问时间。在高速缓存查找期间，将校验和与现有镜像中的校验和进行比较。如果文件中有任何更改（例如内容和元数据），则缓存无效
*   除了`ADD`和`COPY`命令之外，缓存检查不会查看容器中的文件来确定缓存匹配。例如，在处理`RUN apt-get -y update`命令时，不检查容器中更新的文件以确定是否存在缓存命中。在这种情况下，只需使用命令字符串本身来查找匹配项

一旦高速缓存失效，所有后续`Dockerfile`命令都会生成新镜像，并且不使用高速缓存。

## Dockerfile指令

这些建议旨在帮助您创建高效且可维护的`Dockerfile`。

### FROM

[FROM指令的Dockerfile引用](https://docs.docker.com/engine/reference/builder/#from)

尽可能使用当前的官方存储库作为镜像的基础。我们推荐[Alpine镜像，](https://hub.docker.com/_/alpine/)因为它受到严格控制并且尺寸较小（目前小于5 MB），同时仍然是完整的Linux发行版。

### LABEL

[了解对象标签](https://docs.docker.com/config/labels-custom-metadata/)

您可以为镜像添加标签，以帮助按项目组织镜像，记录许可信息，帮助实现自动化或出于其他原因。对于每个标签，添加`LABEL`以一个或多个键值对开头的行。以下示例显示了不同的可接受格式。内容包括解释性意见。

> 带空格的字符串必须用双引用**或**转义空格，引用内字符 `"` 也必须进行转义。

```docker
# Set one or more individual labels
LABEL com.example.version="0.0.1-beta"
LABEL vendor1="ACME Incorporated"
LABEL vendor2=ZENITH\ Incorporated
LABEL com.example.release-date="2015-02-12"
LABEL com.example.version.is-production=""
```

镜像可以有多个标签。在Docker 1.10之前，建议将所有标签组合到一条`LABEL`指令中，以防止创建额外的层。这不再是必需的，但仍然支持组合标签。

```docker
# Set multiple labels on one line
LABEL com.example.version="0.0.1-beta" com.example.release-date="2015-02-12"
```

以上也可以写成：

```docker
# Set multiple labels at once, using line-continuation characters to break long lines
LABEL vendor=ACME\ Incorporated \
      com.example.is-beta= \
      com.example.is-production="" \
      com.example.version="0.0.1-beta" \
      com.example.release-date="2015-02-12"
```

有关可接受的标签键和值的指导，请参阅[了解对象标签](https://docs.docker.com/config/labels-custom-metadata/)。有关查询标​​签的信息，请参阅[管理对象标签中](https://docs.docker.com/config/labels-custom-metadata/#managing-labels-on-objects)与过滤相关的项目。另请参见 Dockerfile参考中的[LABEL](https://docs.docker.com/engine/reference/builder/#label)。

### RUN

[RUN指令的Dockerfile参考](https://docs.docker.com/engine/reference/builder/#run)

`RUN`在使用反斜杠分隔的多行上拆分长或复杂语句，以使您`Dockerfile`更具可读性，可理解性和可维护性。

#### APT-GET

可能最常见的用例`RUN`是应用程序`apt-get`。因为它安装了包，所以该`RUN apt-get`命令有几个需要注意的问题。

避免`RUN apt-get upgrade`和`dist-upgrade`，因为父镜像中的许多“基本”包无法在[非特权容器](https://docs.docker.com/engine/reference/run/#security-configuration)内升级 。如果父镜像中包含的包已过期，请与其维护人员联系。如果您知道有`foo`需要更新的特定包，请使用 `apt-get install -y foo`自动更新。

始终在同一 声明中结合`RUN apt-get update`使用。例如：`apt-get install``RUN`

```docker
    RUN apt-get update && apt-get install -y \
        package-bar \
        package-baz \
        package-foo
```

`apt-get update`在`RUN`语句中单独使用会导致缓存问题，并且后续`apt-get install`指令会失败。例如，假设你有一个Dockerfile：

```docker
    FROM ubuntu:14.04
    RUN apt-get update
    RUN apt-get install -y curl
```

构建镜像后，所有层都在Docker缓存中。假设您稍后`apt-get install`通过添加额外包修改：

```docker
    FROM ubuntu:14.04
    RUN apt-get update
    RUN apt-get install -y curl nginx
```

Docker将初始和修改的指令视为相同，并重用前面步骤中的缓存。其结果是，`apt-get update`在*不*执行，因为编译使用缓存的版本。因为`apt-get update`没有运行，您的构建有可能得到的一个过时的版本`curl`和 `nginx`包。

使用`RUN apt-get update && apt-get install -y`确保您的Dockerfile安装最新的软件包版本，无需进一步编码或手动干预。这种技术称为“缓存清除”。您还可以通过指定包版本来实现缓存清除。这称为版本固定，例如：

```docker
    RUN apt-get update && apt-get install -y \
        package-bar \
        package-baz \
        package-foo=1.3.*
```

版本固定会强制构建以检索特定版本，而不管缓存中的内容是什么。此技术还可以减少由于所需包中的意外更改而导致的故障。

下面是一个结构良好的`RUN`说明，演示了所有`apt-get` 建议。

```docker
RUN apt-get update && apt-get install -y \
    aufs-tools \
    automake \
    build-essential \
    curl \
    dpkg-sig \
    libcap-dev \
    libsqlite3-dev \
    mercurial \
    reprepro \
    ruby1.9.1 \
    ruby1.9.1-dev \
    s3cmd=1.1.* \
 && rm -rf /var/lib/apt/lists/*
```

该`s3cmd`参数指定一个版本`1.1.*`。如果镜像以前使用的是旧版本，则指定新版本会导致缓存破坏，`apt-get update`并确保安装新版本。列出每行的包也可以防止包重复中的错误。

此外，当您通过删除清理apt缓存时，`/var/lib/apt/lists`它会减小镜像大小，因为apt缓存不存储在图层中。由于 `RUN`语句以`apt-get update`开头，因此包缓存始终在`apt-get install`执行之前刷新。

> 官方Debian和Ubuntu镜像[自动运行`apt-get clean`](https://github.com/moby/moby/blob/03e2923e42446dbb830c654d0eec323a0b4ef02a/contrib/mkimage/debootstrap#L82-L105)，因此不需要显式调用。

#### 使用管道

某些`RUN`命令依赖于使用管道符（`|`）将一个命令的输出传递到另一个命令的能力，如下例所示：

```docker
RUN wget -O - https://some.site | wc -l > /number
```

Docker使用`/bin/sh -c`解释器执行这些命令，解释器仅评估管道中最后一个操作的退出代码以确定成功。在上面的示例中，只要`wc -l`命令成功，即使`wget`命令失败，此构建步骤也会成功并生成新镜像。

如果您希望命令因管道中任何阶段的错误而失败，请预先`set -o pipefail &&`确定意外错误可防止构建无意中成功。例如：

```docker
RUN set -o pipefail && wget -O - https://some.site | wc -l > /number

```

> 并非所有shell都支持该`-o pipefail`选项。
> 
> 在这种情况下（例如`dash` shell，它是基于Debian的镜像上的默认shell），请考虑使用*exec*形式`RUN`明确选择支持该`pipefail`选项的shell 。例如：
> 
> ```
> RUN ["/bin/bash", "-c", "set -o pipefail && wget -O - https://some.site | wc -l > /number"]
> ```

### CMD

[CMD指令的Dockerfile参考](https://docs.docker.com/engine/reference/builder/#cmd)

该`CMD`指令应用于运行镜像包含的软件以及任何参数。`CMD`应该几乎总是以`CMD [“executable”, “param1”, “param2”…]`形式使用。因此，如果镜像是用于服务的，例如Apache和Rails，那么你可以运行类似的东西`CMD ["apache2","-DFOREGROUND"]`。实际上，建议将这种形式的指令用于任何基于服务的镜像。

在大多数其他情况下，`CMD`应该给出一个交互式shell，例如bash，python和perl。例如，`CMD ["perl", "-de0"]`，`CMD ["python"]`，或`CMD [“php”, “-a”]`。使用此表单意味着当您执行类似`docker run -it python`的操作时，您将被放入可用的shell中，随时可以使用。`CMD`应该尽量避免的使用`CMD [“param”, “param”]`同[`ENTRYPOINT`](https://docs.docker.com/engine/reference/builder/#entrypoint)一起使用，除非你和你预期的用户已经非常熟悉`ENTRYPOINT`如何工作的。

### EXPOSE

[EXPOSE指令的Dockerfile参考](https://docs.docker.com/engine/reference/builder/#expose)

该`EXPOSE`指令指示容器侦听连接的端口。因此，您应该为您的应用程序使用通用的传统端口。例如，包含Apache Web服务器`EXPOSE 80`的镜像将使用，而包含MongoDB的镜像将使用`EXPOSE 27017`，依此类推。

对于外部访问，您的用户可以`docker run`使用一个标志来执行，该标志指示如何将指定端口映射到他们选择的端口。对于容器链接，Docker为从接收容器返回源的路径提供环境变量（即`MYSQL_PORT_3306_TCP`）。

### ENV

[ENV指令的Dockerfile参考](https://docs.docker.com/engine/reference/builder/#env)

要使新软件更易于运行，您可以使用`ENV`更新`PATH`容器安装的软件的 环境变量。例如，`ENV PATH /usr/local/nginx/bin:$PATH`确保`CMD [“nginx”]` 正常工作。

该`ENV`指令对于提供特定于您希望容纳的服务所需的环境变量也很有用，例如Postgres `PGDATA`。

最后，`ENV`还可以用来设置常用的版本号，以便更容易维护版本颠簸，如下例所示：

```docker
ENV PG_MAJOR 9.3
ENV PG_VERSION 9.3.4
RUN curl -SL http://example.com/postgres-$PG_VERSION.tar.xz | tar -xJC /usr/src/postgress && …
ENV PATH /usr/local/postgres-$PG_MAJOR/bin:$PATH
```

与在程序中使用常量变量（与硬编码值相对）类似，此方法允许您更改单个`ENV`指令以自动神奇地破坏容器中的软件版本。

每`ENV`行创建一个新的中间层，就像`RUN`命令一样。这意味着即使您在将来的图层中取消设置环境变量，它仍然会在此图层中保留，并且可以转储其值。您可以通过创建如下所示的Dockerfile来测试它，然后构建它。

```docker
FROM alpine
ENV ADMIN_USER="mark"
RUN echo $ADMIN_USER > ./mark
RUN unset ADMIN_USER
CMD sh
```

```sh
$ docker run --rm -it test sh echo $ADMIN_USER

mark
```

要防止这种情况，并且确实取消设置环境变量，请使用`RUN`带有shell命令的命令，在单个图层中设置，使用和取消设置变量all。您可以使用`;`或分隔命令`&&`。如果您使用第二种方法，并且其中一个命令失败，则`docker build`也会失败。这通常是一个好主意。使用`\`Linux Dockerfiles作为行继续符可以提高可读性。您还可以将所有命令放入shell脚本中，并让`RUN`命令运行该shell脚本。

```docker
FROM alpine
RUN export ADMIN_USER="mark" \
    && echo $ADMIN_USER > ./mark \
    && unset ADMIN_USER
CMD sh
```

```sh
$ docker run --rm -it test sh echo $ADMIN_USER
```

### ADD或COPY

*   [ADD指令的Dockerfile参考](https://docs.docker.com/engine/reference/builder/#add)
*   [COPY指令的Dockerfile参考](https://docs.docker.com/engine/reference/builder/#copy)

一般而言，虽然`ADD`和`COPY`在功能上类似，但是`COPY` 是优选的。那是因为它比`ADD`更透明。`COPY`仅支持将本地文件复制到容器中，然而`ADD`具有一些功能（如仅限本地的tar提取和远程URL支持），这些功能并不是很明显。因此，`ADD`最好的用途是将本地tar文件自动提取解压到镜像中，如`ADD rootfs.tar.xz /`。

如果您有多个`Dockerfile`步骤使用上下文中的不同文件，则`COPY`它们是单独的，而不是一次性完成。这可确保每个步骤的构建缓存仅在特定所需文件更改时失效（强制重新执行该步骤）。

例如：

```docker
COPY requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt
COPY . /tmp/
```

与`RUN`放置`COPY . /tmp/`之前的步骤相比，该步骤 的缓存失效更少。

由于镜像大小很重要，`ADD`因此强烈建议不要使用从远程URL获取包。你应该使用`curl`或`wget`代替。这样，您可以删除提取后不再需要的文件，也不必在镜像中添加其他图层。例如，你应该避免做以下事情：

```docker
ADD http://example.com/big.tar.xz /usr/src/things/
RUN tar -xJf /usr/src/things/big.tar.xz -C /usr/src/things
RUN make -C /usr/src/things all
```

而是做一些像：

```docker
RUN mkdir -p /usr/src/things \
    && curl -SL http://example.com/big.tar.xz \
    | tar -xJC /usr/src/things \
    && make -C /usr/src/things all

```

对于不需要`ADD`的tar自动提取功能的其他项目（文件，目录），您应该始终使用`COPY`。

### ENTRYPOINT

[ENTRYPOINT指令的Dockerfile参考](https://docs.docker.com/engine/reference/builder/#entrypoint)

最好的用法`ENTRYPOINT`是设置镜像的主命令，允许该镜像像该命令一样运行（然后`CMD`用作默认标志）。

让我们从命令行工具的镜像示例开始`s3cmd`：

```docker
ENTRYPOINT ["s3cmd"]
CMD ["--help"]
```

现在可以像这样运行镜像来显示命令的帮助：

```sh
$ docker run s3cmd
```

或使用正确的参数执行命令：

```sh
$ docker run s3cmd ls s3://mybucket
```

这很有用，因为镜像名称可以兼作二进制文件的引用，如上面的命令所示。

该`ENTRYPOINT`指令还可以与辅助脚本结合使用，使其能够以与上述命令类似的方式运行，即使启动该工具可能需要多个步骤。

例如，[Postgres官方镜像](https://hub.docker.com/_/postgres/) 使用以下脚本作为其`ENTRYPOINT`：

```sh
#!/bin/bash
set -e

if [ "$1" = 'postgres' ]; then
    chown -R postgres "$PGDATA"

    if [ -z "$(ls -A "$PGDATA")" ]; then
        gosu postgres initdb
    fi

    exec gosu postgres "$@"
fi

exec "$@"
```

> 将app配置为PID 1
> 
> 此脚本使用[`exec` bash命令](http://wiki.bash-hackers.org/commands/builtin/exec) ，以使最终运行的应用程序成为容器的PID 1.这允许应用程序接收发送到所述容器任何Unix信号。如需更多信息，请参阅[`ENTRYPOINT`参考](https://docs.docker.com/engine/reference/builder/#entrypoint)。

帮助程序脚本被复制到容器中并通过`ENTRYPOINT`容器启动运行：

```docker
COPY ./docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["postgres"]
```

该脚本允许用户以多种方式与Postgres交互。

它可以简单地启动Postgres：

```sh
$ docker run postgres
```

或者，它可用于运行Postgres并将参数传递给服务器：

```sh
$ docker run postgres postgres --help
```

最后，它还可以用来启动一个完全不同的工具，比如Bash：

```sh
$ docker run --rm -it postgres bash
```

### VOLUME

[VOLUME指令的Dockerfile参考](https://docs.docker.com/engine/reference/builder/#volume)

该`VOLUME`指令应用于公开由docker容器创建的任何数据库存储区域，配置存储或文件/文件夹。强烈建议您在镜像的任何可变和/或用户可维修部分使用`VOLUME`指令。

### USER

[USER指令的Dockerfile参考](https://docs.docker.com/engine/reference/builder/#user)

如果服务可以在没有权限的情况下运行，请使用`USER`更改为非root用户。首先在`Dockerfile`类似的东西中创建用户和组`RUN groupadd -r postgres && useradd --no-log-init -r -g postgres postgres`。

> 考虑一个显式的UID / GID
> 
> 镜像中的用户和组被分配了非确定性UID / GID，因为无论镜像重建如何，都会分配“下一个”UID / GID。因此，如果它很重要，您应该分配一个显式的UID / GID。

> 由于Go archive/tar包处理稀疏文件时[bug](https://github.com/golang/go/issues/13548)，尝试在Docker容器内创建具有非常大的UID的用户可能导致磁盘耗尽，因为`/var/log/faillog`在容器层中填充了NULL（\0）字符。解决方法是将`--no-log-init`标志传递给useradd。Debian / Ubuntu `adduser`包装器不支持此标志。

避免安装或使用`sudo`因为它具有可能导致问题的不可预测的TTY和信号转发行为。如果您一定需要类似的`sudo`功能，例如将守护程序初始化`root`而使用非`root`运行它，请考虑使用[“gosu”](https://github.com/tianon/gosu)。

最后，为了减少层次和复杂性，避免`USER`频繁地来回切换。

### WORKDIR

[WORKDIR指令的Dockerfile参考](https://docs.docker.com/engine/reference/builder/#workdir)

为了清晰和可靠，您应该始终使用绝对路径`WORKDIR`。此外，您应该使用`WORKDIR`而不是难以阅读，故障排除和维护的`RUN cd … && do-something`指令。

### ONBUILD

[ONBUILD指令的Dockerfile参考](https://docs.docker.com/engine/reference/builder/#onbuild)

一个`ONBUILD`命令将在当前`Dockerfile`构建完成之后执行。 `ONBUILD`在任何导出`FROM`当前镜像的子镜像中执行。将`ONBUILD`命令视为父母`Dockerfile`给孩子的指令`Dockerfile`。

Docker构建`ONBUILD`在子代中的任何命令之前执行命令 `Dockerfile`。

`ONBUILD`对于将要构建`FROM`给定镜像的镜像非常有用。例如，您可以使用`ONBUILD`语言堆栈镜像来构建使用该语言编写的任意用户软件`Dockerfile`，正如您在[Ruby的`ONBUILD`变体中所](https://github.com/docker-library/ruby/blob/master/2.4/jessie/onbuild/Dockerfile)看到的那样。

构建的镜像`ONBUILD`应该获得单独的标记，例如： `ruby:1.9-onbuild`或`ruby:2.0-onbuild`。

在`ONBUILD`中小心使用`ADD`或`COPY`。如果新构建的上下文缺少正在添加的资源，则“onbuild”镜像将发生灾难性故障。如上所述，添加单独的标记有助于通过允许`Dockerfile`作者做出选择来缓解这种情况。

## 官方存储库的示例

这些官方存储库具有示范性`Dockerfile`：

*   [GO](https://hub.docker.com/_/golang/)
*   [Perl](https://hub.docker.com/_/perl/)
*   [Hy](https://hub.docker.com/_/hylang/)
*   [Ruby](https://hub.docker.com/_/ruby/)

## 其他资源：

*   [Dockerfile参考](https://docs.docker.com/engine/reference/builder/)
*   [更多关于基本镜像](https://docs.docker.com/develop/develop-images/baseimages/)
*   [有关自动构建的更多信息](https://docs.docker.com/docker-hub/builds/)
*   [创建官方存储库的指南](https://docs.docker.com/docker-hub/official_repos/)

[父镜像](https://docs.docker.com/glossary/?term=parent%20image)，[镜像](https://docs.docker.com/glossary/?term=images)，[dockerfile](https://docs.docker.com/glossary/?term=dockerfile)，[最佳实践](https://docs.docker.com/glossary/?term=best%20practices)，[集线器](https://docs.docker.com/glossary/?term=hub)，[官方回购](https://docs.docker.com/glossary/?term=official%20repo)
