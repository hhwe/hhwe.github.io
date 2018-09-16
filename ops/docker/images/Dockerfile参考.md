# Dockerfile引用

##### [Dockerfile reference](https://docs.docker.com/engine/reference/builder/)

Docker可以通过阅读来自的`Dockerfile`指令自动构建镜像。`Dockerfile`是一个文本文档，其中包含用户可以在命令行上调用以组合镜像的所有命令。使用`docker build` 用户可以创建一个连续执行多个命令行指令的自动构建。

本页介绍了可以在中使用的命令`Dockerfile`。阅读完本页后，请参阅[`Dockerfile`最佳实践](https://docs.docker.com/engine/userguide/eng-image/dockerfile_best-practices/)以获取面向技巧的指南。

## 用法

[`docker build`](https://docs.docker.com/engine/reference/commandline/build/)指令是`Dockerfile`根据*上下文*构建镜像，构建的上下文是指定位置`PATH`或的文件集`URL`。这`PATH`是本地文件系统上的目录，而`URL`是一个Git存储库位置。

递归处理上下文。因此，`PATH`包括所有子目录，`URL`包括存储库及其子模块。此示例显示了使用当前目录作为上下文的构建命令：

```
$ docker build .
Sending build context to Docker daemon  6.51 MB
...
```

构建由Docker守护程序运行，而不是由CLI运行。构建过程的第一件事是将整个上下文（递归地）发送到守护进程。在大多数情况下，最好从空目录开始作为上下文，并将Dockerfile保存在该目录中。仅添加构建Dockerfile所需的文件。

> **警告**：不要用你的根目录下，`/`作为`PATH`因为它会导致生成到您的硬盘驱动器的全部内容传输到码头工人守护进程。

要在构建上下文中使用文件，请`Dockerfile`引用指令中指定的文件，例如`COPY`指令。要提高构建的性能，请通过向`.dockerignore`上下文目录添加文件来排除文件和目录。有关如何[创建`.dockerignore` 文件的信息，](https://docs.docker.com/engine/reference/builder/#dockerignore-file)请参阅此页面上的文档。

传统上，它`Dockerfile`被调用`Dockerfile`并位于上下文的根中。您可以使用`-f`标志`docker build`指向文件系统中任何位置的Dockerfile。

```
$ docker build -f /path/to/a/Dockerfile .
```

您可以指定存储库和标记以保存新镜像：

```
$ docker build -t shykes/myapp .
```

要在构建后将镜像标记为多个存储库，请在`-t`运行`build`命令时添加多个参数：

```
$ docker build -t shykes/myapp:1.0.2 -t shykes/myapp:latest .
```

在Docker守护程序运行`Dockerfile`其中的指令之前，它会执行初步验证`Dockerfile`并在语法不正确时返回错误：

```
$ docker build -t test/myapp .
Sending build context to Docker daemon 2.048 kB
Error response from daemon: Unknown instruction: RUNCMD
```

Docker守护程序逐个运行`Dockerfile`指令，在必要时将每条指令的结果提交给新镜像，最后输出新镜像的ID。Docker守护程序将自动清理您发送的上下文。

请注意，每条指令都是独立运行的，会导致创建新镜像 - 因此`RUN cd /tmp`不会对下一条指令产生任何影响。

只要有可能，Docker将重新使用中间镜像（缓存），以`docker build`显着加速该过程。这由`Using cache`控制台输出中的消息指示。（有关详细信息，请参阅[构建高速缓存段](https://docs.docker.com/engine/userguide/eng-image/dockerfile_best-practices/#build-cache)的 `Dockerfile`最佳实践指南）：

```
$ docker build -t svendowideit/ambassador .
Sending build context to Docker daemon 15.36 kB
Step 1/4 : FROM alpine:3.2
 ---> 31f630c65071
Step 2/4 : MAINTAINER SvenDowideit@home.org.au
 ---> Using cache
 ---> 2a1c91448f5f
Step 3/4 : RUN apk update &&      apk add socat &&        rm -r /var/cache/
 ---> Using cache
 ---> 21ed6e7fbb73
Step 4/4 : CMD env | grep _TCP= | (sed 's/.*_PORT_\([0-9]*\)_TCP=tcp:\/\/\(.*\):\(.*\)/socat -t 100000000 TCP4-LISTEN:\1,fork,reuseaddr TCP4:\2:\3 \&/' && echo wait) | sh
 ---> Using cache
 ---> 7ea8aef582cc
Successfully built 7ea8aef582cc
```

构建缓存仅用于具有本地父链的镜像。这意味着这些镜像是由以前的版本创建的，或者加载了整个镜像链`docker load`。如果您希望使用特定镜像的构建缓存，可以使用`--cache-from`选项指定它。指定的镜像 `--cache-from`不需要具有父链，可以从其他注册表中提取。

完成构建后，您已准备好查看[*将存储库推送到其注册表*](https://docs.docker.com/engine/tutorials/dockerrepos/#/contributing-to-docker-hub)。

## 格式

这是以下格式`Dockerfile`：

```
# Comment
INSTRUCTION arguments
```

该指令不区分大小写。但是，惯例是让它们成为大写的，以便更容易地将它们与参数区分开来。

Docker按顺序运行`Dockerfile`指令。一个`Dockerfile`**必须用`FROM`指令开头**。该`FROM`指令指定您正在构建的[*基本镜像*](https://docs.docker.com/engine/reference/glossary/#base-image)。`FROM`可以在一个或多个`ARG`的指令前面，其声明了在使用的参数`FROM`中的行`Dockerfile`。

Docker 将以`#`*开头的*行视为注释，除非该行是有效的[解析器指令](https://docs.docker.com/engine/reference/builder/#parser-directives)。`#`行中任何其他位置的标记都被视为参数。这允许这样的陈述：

```
# Comment
RUN echo 'we are running some # of cool things'
```

注释中不支持行继续符。

## 解析器指令

解析器指令是可选的，并且影响`Dockerfile`处理后续行的方式。解析器指令不会向构建添加图层，也不会显示为构建步骤。解析器指令在表单中被写为特殊类型的注释`# directive=value`。单个指令只能使用一次。

一旦处理了注释，空行或构建器指令，Docker就不再查找解析器指令。相反，它将格式化为解析器指令的任何内容视为注释，并且不会尝试验证它是否可能是解析器指令。因此，所有解析器指令必须位于`Dockerfile`的顶部。

分析器指令不区分大小写。但是，惯例是它们是小写的。约定还包括任何解析器指令后面的空行。解析器指令不支持行继续符。

由于这些规则，以下示例均无效：

由于行继续而无效：

```
# direc \
tive=value
```

由于出现两次无效：

```
# directive=value1
# directive=value2

FROM ImageName
```

由于在构建器指令后出现而被视为注释：

```
FROM ImageName
# directive=value
```

由于不在解析器指令的注释之后出现而被视为注释：

```
# About my dockerfile
# directive=value
FROM ImageName
```

由于未被识别，未知指令被视为注释。此外，由于出现在不是解析器指令的注释之后，已知指令被视为注释。

```
# unknowndirective=value
# knowndirective=value
```

解析器指令中允许使用非换行空格。因此，以下几行都是相同的：

```
#directive=value
# directive =value
#	directive= value
# directive = value
#	  dIrEcTiVe=value
```

支持以下解析器指令：

*   `escape`

## escape

```
# escape=\ (backslash)
```

要么

```
# escape=` (backtick)
```

该`escape`指令设置用于转义字符的字符 `Dockerfile`。如果未指定，则默认转义字符为`\`。

转义字符既用于转义行中的字符，也用于转义换行符。这允许`Dockerfile`指令跨越多行。请注意，无论`escape`解析器指令是否包含在a中`Dockerfile`，*都不会在`RUN`命令中执行转义，除非在行的末尾。*

将转义字符设置```在`Windows`中特别有用，`Windows`中`\`为目录路径分隔符```与[Windows PowerShell](https://technet.microsoft.com/en-us/library/hh847755.aspx)一致。

请考虑以下示例，该示例将以非显而易见的方式失败 `Windows`。第二`\`，在第二行的端部将被解释为用于换行的逃逸，而不是从第一逸出的目标`\`。类似地，`\`在第三行的末尾，假设它实际上作为指令处理，将导致它被视为行继续。这个dockerfile的结果是第二行和第三行被认为是单个指令：

```
FROM microsoft/nanoserver
COPY testfile.txt c:\\
RUN dir c:\
```

结果是：

```
PS C:\John> docker build -t cmd .
Sending build context to Docker daemon 3.072 kB
Step 1/2 : FROM microsoft/nanoserver
 ---> 22738ff49c6d
Step 2/2 : COPY testfile.txt c:\RUN dir c:
GetFileAttributesEx c:RUN: The system cannot find the file specified.
PS C:\John>
```

上面的一个解决方案是`/`用作`COPY` 指令的目标，和`dir`。但是，这种语法充其量是令人困惑的，因为对于路径来说并不自然`Windows`，并且最坏的情况是容易出错，因为并非所有命令都 作为路径分隔符`Windows`支持`/`。

通过添加`escape`解析器指令，以下`Dockerfile`成功使用文件路径的自然平台语义`Windows`：

```
# escape=`

FROM microsoft/nanoserver
COPY testfile.txt c:\
RUN dir c:\
```

结果是：

```
PS C:\John> docker build -t succeeds --no-cache=true .
Sending build context to Docker daemon 3.072 kB
Step 1/3 : FROM microsoft/nanoserver
 ---> 22738ff49c6d
Step 2/3 : COPY testfile.txt c:\
 ---> 96655de338de
Removing intermediate container 4db9acbb1682
Step 3/3 : RUN dir c:\
 ---> Running in a2c157f842f5
 Volume in drive C has no label.
 Volume Serial Number is 7E6D-E0F7

 Directory of c:\

10/05/2016  05:04 PM             1,894 License.txt
10/05/2016  02:22 PM    <DIR>          Program Files
10/05/2016  02:14 PM    <DIR>          Program Files (x86)
10/28/2016  11:18 AM                62 testfile.txt
10/28/2016  11:20 AM    <DIR>          Users
10/28/2016  11:20 AM    <DIR>          Windows
           2 File(s)          1,956 bytes
           4 Dir(s)  21,259,096,064 bytes free
 ---> 01c7f3bef04f
Removing intermediate container a2c157f842f5
Successfully built 01c7f3bef04f
PS C:\John>
```

## 环境更换

环境变量（与声明[的`ENV`声明](https://docs.docker.com/engine/reference/builder/#env)），也可以在特定指令作为变量用来被解释 `Dockerfile`。还会处理转义，以便将类似变量的语法包含在字面上。

在`Dockerfile`中环境变量用 `$variable_name`或者`${variable_name}`表示。它们被等效地处理，并且括号语法通常用于解决具有没有空格的变量名称的问题，例如`${foo}_bar`。

该`${variable_name}`语法还支持一些标准的`bash` 修饰如下规定：

*   `${variable:-word}`表示if `variable`设置后，结果将是该值。如果`variable`未设置则`word`结果将是
*   `${variable:+word}`表示如果`variable`设置，那么`word`将是结果，否则结果是空字符串

在所有情况下，`word`可以是任何字符串，包括其他环境变量。

通过`\`在变量之前添加a来实现转义：`\$foo`或者`\${foo}`，例如，将分别转换为`$foo`和`${foo}`文本。

示例（解析后的表示显示在`#`）之后：

```
FROM busybox
ENV foo /bar
WORKDIR ${foo}   # WORKDIR /bar
ADD . $foo       # ADD . /bar
COPY \$foo /quux # COPY $foo /quux
```

以下指令列表支持环境变量`Dockerfile`：

*   `ADD`
*   `COPY`
*   `ENV`
*   `EXPOSE`
*   `FROM`
*   `LABEL`
*   `STOPSIGNAL`
*   `USER`
*   `VOLUME`
*   `WORKDIR`

以及：

*   `ONBUILD` （当与上面支持的指令之一结合使用时）

> **注意**：在1.4之前，`ONBUILD`指令**不**支持环境变量，即使与上面列出的任何指令结合使用也是如此。

环境变量替换将在整个指令中对每个变量使用相同的值。换句话说，在这个例子中：

```
ENV abc=hello
ENV abc=bye def=$abc
ENV ghi=$abc
```

将导致`def`具有值`hello`，而不是`bye`。但是， `ghi`将具有值，`bye`因为它不是设置`abc`为的相同指令的一部分`bye`。

## .dockerignore文件

在docker CLI将上下文发送到docker守护程序之前，它会查找`.dockerignore`在上下文的根目录中指定的文件。如果此文件存在，CLI将修改上下文以排除与其中的模式匹配的文件和目录。这有助于避免不必要地将大型或敏感文件和目录发送到守护程序，并可能使用`ADD`或将它们添加到镜像中`COPY`。

CLI将该`.dockerignore`文件解释为新行分隔的模式列表，类似于Unix shell的文件globs。出于匹配的目的，上下文的根被认为是工作目录和根目录。例如，模式 `/foo/bar`和`foo/bar`两者都排除`bar`在位于的git存储库的`foo`子目录`PATH`或根目录中命名的文件或目录`URL`。两者都不包括任何其他内容。

如果`.dockerignore`文件中的行以第`#`1列开头，则此行被视为注释，并在CLI解释之前被忽略。

这是一个示例`.dockerignore`文件：

```
# comment
*/temp*
*/*/temp*
temp?

```

此文件导致以下构建行为：

| 规则 | 行为 |
| --- | --- |
| `# comment` | 忽略。 |
| `*/temp*` | 排除名称以`temp`根目录的任何直接子目录开头的文件和目录。例如，`/somedir/temporary.txt`排除普通文件，目录也是如此`/somedir/temp`。 |
| `*/*/temp*` | 排除`temp`从根目录下两级开始的任何子目录开始的文件和目录。例如，`/somedir/subdir/temporary.txt`被排除在外。 |
| `temp?` | 排除根目录中的文件和目录，其名称是单字符扩展名`temp`。例如，`/tempa`与`/tempb`被排除在外。 |

匹配是使用Go的 [filepath.Match](http://golang.org/pkg/path/filepath#Match)规则完成的。预处理步骤去除了开头和结尾的空白，并消除`.`与`..`使用Go的元素 [filepath.Clean](http://golang.org/pkg/path/filepath/#Clean)。预处理后为空的行将被忽略。

除了Go的filepath.Match规则，Docker还支持一个`**`匹配任意数量目录（包括零）的特殊通配符字符串。例如，`**/*.go`将排除`.go` 在所有目录中找到的以该结尾的所有文件，包括构建上下文的根。

以`!`（感叹号）开头的行可用于对排除项进行例外处理。以下是`.dockerignore`使用此机制的示例文件：

```
    *.md
    !README.md
```

除`README.md`外，所有md文件会排除在上下文。

`!`异常规则的放置会影响行为：`.dockerignore`匹配特定文件的最后一行确定是包含还是排除。请考虑以下示例：

```
    *.md
    !README*.md
    README-secret.md
```

除了README开头的md文件以外，上下文中不包含任何markdown文件包括README-secret.md。

现在考虑这个例子：

```
    *.md
    README-secret.md
    !README*.md
```

包含所有README开头的md文件。中间行没有效果，因为 `!README*.md`匹配`README-secret.md`并且是最后的。

您甚至可以使用该`.dockerignore`文件来排除`Dockerfile` 和`.dockerignore`文件。这些文件仍然发送到守护程序，因为它需要它们来完成它的工作。但是`ADD`和`COPY`指令不会将它们复制到镜像中。

最后，您可能希望指定要包含在上下文中的文件，而不是要排除的文件。要实现此目的，请指定`*`第一个模式，然后指定一个或多个`!`异常模式。

**注意**：由于历史原因，将`.`忽略该模式。

## FROM

```
FROM <image> [AS <name>]
```

要么

```
FROM <image>[:<tag>] [AS <name>]
```

要么

```
FROM <image>[@<digest>] [AS <name>]
```

该`FROM`指令初始化新的构建阶段并为后续指令设置 [*基本镜像*](https://docs.docker.com/engine/reference/glossary/#base-image)。因此，有效`Dockerfile`必须以`FROM`指令开始。镜像可以是任何有效镜像 - 通过从[*公共存储库中*](https://docs.docker.com/engine/tutorials/dockerrepos/)**提取镜像**来启动它尤其容易。[](https://docs.docker.com/engine/tutorials/dockerrepos/)

*   `ARG`是先于仅指示`FROM`在`Dockerfile`。请参阅[了解ARG和FROM如何交互](https://docs.docker.com/engine/reference/builder/#understand-how-arg-and-from-interact)。

*   `FROM`可以在一个单独中出现多次`Dockerfile`以创建多个镜像或使用一个构建阶段作为另一个构建阶段的依赖项。只需在每条新`FROM`指令之前记下提交输出的最后一个镜像ID 。每条`FROM`指令都清除先前指令创建的任何状态。

*   可选地，可以通过添加`AS name`到`FROM`指令来将 名称赋予新的构建阶段。该名称可用于后续`FROM`和 `COPY --from=<name|index>`指令，以引用此阶段构建的镜像。

*   该`tag`或`digest`值是可选的。如果省略其中任何一个，则构建器默认采用`latest`标记。如果找不到`tag`值，构建器将返回错误。

### 了解ARG和FROM如何互动

`FROM`说明支持由`ARG` 第一个之前发生的任何指令声明的变量`FROM`。

```
ARG  CODE_VERSION=latest
FROM base:${CODE_VERSION}
CMD  /code/run-app

FROM extras:${CODE_VERSION}
CMD  /code/run-extras
```

在`ARG`宣布之前，`FROM`是一个构建阶段之外，因此它不能在之后的任何指令使用`FROM`。要`ARG`在第一次`FROM`使用之前使用声明的默认值，请在`ARG`构建阶段内使用没有值的指令：

```
ARG VERSION=latest
FROM busybox:$VERSION
ARG VERSION
RUN echo $VERSION > image_version

```

## RUN

RUN有两种形式：

*   `RUN <command>`（*shell*表单，该命令在shell中运行，默认情况下`/bin/sh -c`在Linux或`cmd /S /C`Windows 上运行）
*   `RUN ["executable", "param1", "param2"]`（*执行*形式）

该`RUN`指令将在当前镜像之上的新层中执行任何命令并提交结果。生成的提交镜像将用于下一步`Dockerfile`。

分层`RUN`指令和生成提交符合Docker的核心概念，其中提交很便宜，并且可以从镜像历史中的任何点创建容器，就像源代码控制一样。

在*EXEC*形式使得能够避免壳串改写（munging），并`RUN` 使用不包含指定壳可执行基本镜像命令。

可以使用该 命令更改*shell*表单的默认shell `SHELL`。

在*shell*形式中，您可以使用`\`（反斜杠）将单个RUN指令继续到下一行。例如，考虑以下两行：

```
RUN /bin/bash -c 'source $HOME/.bashrc; \
echo $HOME'
```

它们一起相当于这一行：

```
RUN /bin/bash -c 'source $HOME/.bashrc; echo $HOME'
```

> **注意**：要使用除“/ bin / sh”之外的其他shell，请使用传入所需shell 的*exec*表单。例如，`RUN ["/bin/bash", "-c", "echo hello"]`
> **注意**：*exec*表单被解析为JSON数组，这意味着您必须使用双引号（“）来围绕单词而不是单引号（'）
>
> **注意**：与*shell*表单不同，*exec*表单不会调用命令shell。这意味着不会发生正常的shell处理。例如， `RUN [ "echo", "$HOME" ]`不会对变量进行替换`$HOME`。如果你想要shell处理，那么要么使用*shell*表单，要么直接执行shell，例如：`RUN [ "sh", "-c", "echo $HOME" ]`。当使用exec表单并直接执行shell时，就像shell表单的情况一样，它是执行环境变量扩展的shell，而不是docker。
> 
> **注意**：在*JSON*表单中，必须转义反斜杠。这在反斜杠是路径分隔符的Windows上尤为重要。由于不是有效的JSON，以下行将被视为*shell*表单，并以意外方式失败：`RUN ["c:\windows\system32\tasklist.exe"]` 此示例的正确语法是：`RUN ["c:\\windows\\system32\\tasklist.exe"]`

`RUN`在下一次构建期间，指令的缓存不会自动失效。类似指令的缓存`RUN apt-get dist-upgrade -y`将在下一次构建期间重用。例如，`RUN`可以通过使用`--no-cache`标志使指令的高速缓存无效`docker build --no-cache`。

有关详细信息，请参阅“ [`Dockerfile`最佳实践指南](https://docs.docker.com/engine/userguide/eng-image/dockerfile_best-practices/#/build-cache) ”。

`RUN`指令的高速缓存可以通过`ADD`指令无效。请参阅 [下文](https://docs.docker.com/engine/reference/builder/#add)了解详情。

### 已知问题（RUN）

*   [问题783](https://github.com/docker/docker/issues/783)是关于使用AUFS文件系统时可能发生的文件权限问题。例如，您可能会在尝试`rm`文件时注意到它。

    对于具有最新aufs版本的系统（即`dirperm1`可以设置挂载选项），docker将尝试通过使用`dirperm1`选项安装图层来自动修复问题。有关`dirperm1`选项的更多详细信息，请参见[`aufs`手册页](https://github.com/sfjro/aufs3-linux/tree/aufs3.18/Documentation/filesystems/aufs)

    如果您的系统不支持`dirperm1`，则问题描述了一种解决方法。

## CMD

该`CMD`指令有三种形式：

*   `CMD ["executable","param1","param2"]`（*exec*形式，这是首选形式）
*   `CMD ["param1","param2"]`（作为*ENTRYPOINT的默认参数*）
*   `CMD command param1 param2`（*shell*形式）

`Dockerfile`中只能有一条`CMD`指令。如果列出多个，`CMD` 则只有最后一个`CMD`生效。

**`CMD`的主要目的是为执行容器提供默认值。**这些默认值可以包含可执行文件，也可以省略可执行文件，在这种情况下，您还必须指定一条`ENTRYPOINT` 指令。

> **注意**：如果`CMD`用于为`ENTRYPOINT` 指令提供默认参数，则应使用JSON数组格式指定`CMD`和`ENTRYPOINT`指令

> **注意**：*exec*表单被解析为JSON数组，这意味着您必须使用双引号（“）来围绕单词而不是单引号（'）

> **注意**：与*shell*表单不同，*exec*表单不会调用命令shell。这意味着不会发生正常的shell处理。例如， `CMD [ "echo", "$HOME" ]`不会对变量进行替换`$HOME`。如果你想要shell处理，那么要么使用*shell*表单，要么直接执行shell，例如：`CMD [ "sh", "-c", "echo $HOME" ]`。当使用exec表单并直接执行shell时，就像shell表单的情况一样，它是执行环境变量扩展的shell，而不是docker

在shell或exec格式中使用时，该`CMD`指令设置在运行镜像时要执行的命令。

如果你使用的是*shell的*形式`CMD`，那么`<command>`将执行 `/bin/sh -c`：

```
FROM ubuntu
CMD echo "This is a test." | wc -
```

如果要**在** `<command>` **没有shell ****的****情况下****运行，**则必须将该命令表示为JSON数组，并提供可执行文件的完整路径。 **此数组形式是首选格式`CMD`。**任何其他参数必须在数组中单独表示为字符串：

```
FROM ubuntu
CMD ["/usr/bin/wc", "--help"]
```

如果您希望容器每次都运行相同的可执行文件，那么您应该考虑`ENTRYPOINT`结合使用`CMD`。请参阅[*ENTRYPOINT*](https://docs.docker.com/engine/reference/builder/#entrypoint)。

如果用户指定了参数，`docker run`那么它们将覆盖指定的默认值`CMD`。

> **注意**：不要混淆`RUN`使用`CMD`。`RUN`实际上运行一个命令并提交结果; `CMD`在构建时不执行任何操作，但指定镜像的预期命令。

## 标签

```
LABEL <key>=<value> <key>=<value> <key>=<value> ...
```

该`LABEL`指令将元数据添加到镜像。A `LABEL`是键值对。要在`LABEL`值中包含空格，请使用引号和反斜杠，就像在命令行解析中一样。一些用法示例：

```
LABEL "com.example.vendor"="ACME Incorporated"
LABEL com.example.label-with-value="foo"
LABEL version="1.0"
LABEL description="This text illustrates \
that label-values can span multiple lines."
```

镜像可以有多个标签。您可以在一行中指定多个标签。在Docker 1.10之前，这减小了最终镜像的大小，但现在不再是这种情况了。您仍然可以选择在单个指令中指定多个标签，方法有以下两种：

```
LABEL multi.label1="value1" multi.label2="value2" other="value3"
```

```
LABEL multi.label1="value1" \
      multi.label2="value2" \
      other="value3"
```

基本或父镜像中包含的标签（`FROM`线中的镜像）由镜像继承。如果标签已存在但具有不同的值，则最近应用的值将覆盖任何先前设置的值。

要查看镜像的标签，请使用该`docker inspect`命令。

```
"Labels": {
    "com.example.vendor": "ACME Incorporated"
    "com.example.label-with-value": "foo",
    "version": "1.0",
    "description": "This text illustrates that label-values can span multiple lines.",
    "multi.label1": "value1",
    "multi.label2": "value2",
    "other": "value3"
},
```

## MAINTAINER（已弃用）

```
MAINTAINER <name>
```

该`MAINTAINER`指令设置生成的镜像的*Author*字段。该`LABEL`指令是一个更加灵活的版本，您应该使用它，因为它可以设置您需要的任何元数据，并且可以轻松查看，例如使用`docker inspect`。要设置与`MAINTAINER`您可以使用的字段对应的标签 ：

```
LABEL maintainer="SvenDowideit@home.org.au"
```

然后可以从`docker inspect`其他标签中看到这一点。

## EXPOSE

```
EXPOSE <port> [<port>/<protocol>...]
```

该`EXPOSE`指令通知Docker容器在运行时侦听指定的网络端口。您可以指定端口是侦听TCP还是UDP，如果未指定协议，则默认为TCP。

该`EXPOSE`指令实际上没有发布端口。它作为构建镜像的人和运行容器的人之间的一种文档，用于发布要发布的端口。要在运行容器时实际发布端口，请使用`-p`标志on `docker run` 来发布和映射一个或多个端口，或使用`-P`标志发布所有公开的端口并将它们映射到高阶端口。

默认情况下，`EXPOSE`假定为TCP。您还可以指定UDP：

```
EXPOSE 80/udp
```

要在TCP和UDP上公开，请包含两行：

```
EXPOSE 80/tcp
EXPOSE 80/udp
```

在这种情况下，如果使用`-P`with `docker run`，端口将为TCP暴露一次，对UDP则暴露一次。请记住，`-P`在主机上使用短暂的高阶主机端口，因此TCP和UDP的端口不同。

无论`EXPOSE`设置如何，您都可以使用`-p`标志在运行时覆盖它们。例如

```
docker run -p 80:80/tcp -p 80:80/udp ...
```

要在主机系统上设置端口重定向，请参阅[使用-P标志](https://docs.docker.com/engine/reference/run/#expose-incoming-ports)。该`docker network`命令支持为容器之间的通信创建网络，而无需公开或发布特定端口，因为连接到网络的容器可以通过任何端口相互通信。有关详细信息，请参阅[此功能](https://docs.docker.com/engine/userguide/networking/)的 [概述](https://docs.docker.com/engine/userguide/networking/)）。

## ENV

```
ENV <key> <value>
ENV <key>=<value> ...
```

该`ENV`指令将环境变量`<key>`设置为该值 `<value>`。此值将在构建阶段中所有后续指令的环境中，并且也可以在许多[内联替换](https://docs.docker.com/engine/reference/builder/#environment-replacement)。

该`ENV`指令有两种形式。第一种形式，`ENV <key> <value>`将一个变量设置为一个值。第一个空格后的整个字符串将被视为`<value>`- 包括空格字符。该值将针对其他环境变量进行解释，因此如果未对其进行转义，则将删除引号字符。

第二种形式`ENV <key>=<value> ...`允许一次设置多个变量。请注意，第二种形式在语法中使用等号（=），而第一种形式则不然。与命令行解析一样，引号和反斜杠可用于在值内包含空格。

例如：

```
ENV myName="John Doe" myDog=Rex\ The\ Dog \
    myCat=fluffy
```

和

```
ENV myName John Doe
ENV myDog Rex The Dog
ENV myCat fluffy
```

将在最终镜像中产生相同的净结果。

`ENV`当从生成的镜像运行容器时，使用的环境变量将保持不变。您可以使用`docker inspect`，查看值，并使用它们进行更改`docker run --env <key>=<value>`。

> **注意**：环境持久性可能会导致意外的副作用。例如，设置`ENV DEBIAN_FRONTEND noninteractive`可能会使基于Debian的镜像上的apt-get用户感到困惑。要为单个命令设置值，请使用 `RUN <key>=<value> <command>`。

## ADD

ADD有两种形式：

*   `ADD [--chown=<user>:<group>] <src>... <dest>`
*   `ADD [--chown=<user>:<group>] ["<src>",... "<dest>"]` （包含空格的路径需要此表单）

> **注意**：该`--chown`功能仅在用于构建Linux容器的Dockerfiles上受支持，并且不适用于Windows容器。由于用户和组所有权概念不能在Linux和Windows之间进行转换，因此使用`/etc/passwd`和`/etc/group`将用户名和组名转换为ID会限制此功能仅适用于基于Linux OS的容器。

`ADD`指令可以中复制新文件，目录或远程文件URL `<src>` ，并将它们添加到镜像的文件系统中`<dest>`路径上。

`<src>`可以指定多个资源，但如果它们是文件或目录，则它们的路径将被解释为相对于构建上下文的源。

每个`<src>`都可能包含通配符，匹配将使用Go的 [filepath.Match](http://golang.org/pkg/path/filepath#Match)规则完成。例如：

```
ADD hom* /mydir/        # adds all files starting with "hom"
ADD hom?.txt /mydir/    # ? is replaced with any single character, e.g., "home.txt"
```

的`<dest>`是一个绝对路径，或相对于一个路径`WORKDIR`，到其中的源将在目标容器内进行复制。

```
ADD test relativeDir/          # adds "test" to `WORKDIR`/relativeDir/
ADD test /absoluteDir/         # adds "test" to /absoluteDir/
```

添加包含特殊字符（例如`[` 和`]`）的文件或目录时，需要按照Golang规则转义这些路径，以防止它们被视为匹配模式。例如，要添加名`arr[0].txt`为的文件，请使用以下命令;

```
ADD arr[[]0].txt /mydir/    # copy a file named "arr[0].txt" to /mydir/
```

除非可选`--chown`标志指定给定用户名，组名或UID/GID组合以请求所添加内容的特定所有权，否则将使用UID和GID为0创建所有新文件和目录。`--chown`标志的格式允许用户名和组名字符串或任意组合的直接整数UID和GID。提供没有组名的用户名或没有GID的UID将使用与GID相同的数字UID。如果提供了用户名或组名，则容器的根文件系统 `/etc/passwd`和`/etc/group`文件将分别用于执行从名称到整数UID或GID的转换。以下示例显示了该`--chown`标志的有效定义：

```
ADD --chown=55:mygroup files* /somedir/
ADD --chown=bin files* /somedir/
ADD --chown=1 files* /somedir/
ADD --chown=10:11 files* /somedir/
```

如果容器根文件系统不包含任何文件`/etc/passwd`或 `/etc/group`文件，并且`--chown` 标志中使用了用户名或组名，则构建将在`ADD`操作上失败。使用数字ID不需要查找，也不依赖于容器根文件系统内容。

在`<src>`远程文件URL 的情况下，目标将具有600的权限。如果正在检索的远程文件具有HTTP`Last-Modified`标头，则来自该标头的时间戳将用于设置`mtime`目标文件。但是，与在处理期间处理的任何其他文件一样`ADD`，`mtime`将不包括在确定文件是否已更改且应更新缓存中。

> **注意**：如果通过传递`Dockerfile`STDIN（`docker build - < somefile`）进行构建，则没有构建上下文，因此`Dockerfile` 只能包含基于URL的`ADD`指令。您还可以通过STDIN :( `docker build - < archive.tar.gz`）传递压缩存档`Dockerfile`，该存档位于存档的根目录，其余存档将用作构建的上下文。

> **注意**：如果您的网址文件都使用认证保护，您将需要使用`RUN wget`，`RUN curl`或使用其它工具从容器内的`ADD`指令不支持验证。

> **注意**：`ADD`如果内容`<src>`已更改，则第一个遇到的指令将使来自Dockerfile的所有后续指令的高速缓存无效。这包括使缓存无效以获取`RUN`指令。有关详细信息，请参阅“ [`Dockerfile`最佳实践指南](https://docs.docker.com/engine/userguide/eng-image/dockerfile_best-practices/#/build-cache) ”。

`ADD` 遵守以下规则：

*   该`<src>`路径必须是内部*语境*的构建; 你不能`ADD ../something /something`，因为`docker build`的第一步是将上下文目录（和子目录）发送到docker守护程序。

*   如果`<src>`是URL并且`<dest>`不以尾部斜杠结尾，则从URL下载文件并将其复制到`<dest>`。

*   如果`<src>`是URL并且`<dest>`以尾部斜杠结尾，则从URL推断文件名并将文件下载到`<dest>/<filename>`。例如，`ADD http://example.com/foobar /`将创建该文件`/foobar`。URL必须具有非常重要的路径，以便在这种情况下可以发现适当的文件名（`http://example.com` 不起作用）。

*   如果`<src>`是目录，则复制目录的全部内容，包括文件系统元数据。

> **注意**：不复制目录本身，只复制其内容。

*   如果`<src>`是以可识别的压缩格式（identity，gzip，bzip2或xz）的*本地* tar存档，则将其解压缩为目录。从资源*远程*网址**不**解压。复制或解压缩目录时，它具有与之相同的行为`tar -x`，结果是：

    1.  无论在目的地路径上存在什么，
    2.  源树的内容，在逐个文件的基础上解决了有利于“2.”的冲突。

    > **注意**：文件是否被识别为可识别的压缩格式仅基于文件的内容而不是文件的名称来完成。例如，如果一个空文件碰巧结束，`.tar.gz`这将不会被识别为压缩文件，并且**不会**生成任何类型的解压缩错误消息，而是将文件简单地复制到目标。

*   如果`<src>`是任何其他类型的文件，则将其与元数据一起单独复制。在这种情况下，如果`<dest>`以尾部斜杠结尾`/`，则将其视为目录，`<src>`并将写入内容`<dest>/base(<src>)`。

*   如果`<src>`直接或由于使用通配符指定了多个资源，则`<dest>`必须是目录，并且必须以斜杠结尾`/`。

*   如果`<dest>`不以尾部斜杠结束，则将其视为常规文件，`<src>`并将写入其中的内容`<dest>`。

*   如果`<dest>`不存在，则会在其路径中创建所有缺少的目录。

## COPY

COPY有两种形式：

*   `COPY [--chown=<user>:<group>] <src>... <dest>`
*   `COPY [--chown=<user>:<group>] ["<src>",... "<dest>"]` （包含空格的路径需要此表单）

> **注意**：该`--chown`功能仅在用于构建Linux容器的Dockerfiles上受支持，并且不适用于Windows容器。由于用户和组所有权概念不能在Linux和Windows之间进行转换，因此使用`/etc/passwd`和`/etc/group`将用户名和组名转换为ID会限制此功能仅适用于基于Linux OS的容器。

该`COPY`指令从中复制新文件或目录`<src>` ，并将它们添加到路径中容器的文件系统中`<dest>`。

`<src>`可以指定多个资源，但文件和目录的路径将被解释为相对于构建上下文的源。

每个都`<src>`可能包含通配符，匹配将使用Go的 [filepath.Match](http://golang.org/pkg/path/filepath#Match)规则完成。例如：

```
COPY hom* /mydir/        # adds all files starting with "hom"
COPY hom?.txt /mydir/    # ? is replaced with any single character, e.g., "home.txt"
```

的`<dest>`是一个绝对路径，或相对于一个路径`WORKDIR`，到其中的源将在目标容器内进行复制。

```
COPY test relativeDir/   # adds "test" to `WORKDIR`/relativeDir/
COPY test /absoluteDir/  # adds "test" to /absoluteDir/
```

复制包含特殊字符（例如`[` 和`]`）的文件或目录时，需要按照Golang规则转义这些路径，以防止它们被视为匹配模式。例如，要复制名为的文件`arr[0].txt`，请使用以下命令;

```
COPY arr[[]0].txt /mydir/    # copy a file named "arr[0].txt" to /mydir/
```

除非可选`--chown`标志指定给定用户名，组名或UID / GID组合以请求复制内容的特定所有权，否则将使用UID和GID为0创建所有新文件和目录。`--chown`标志的格式允许用户名和组名字符串或任意组合的直接整数UID和GID。提供没有组名的用户名或没有GID的UID将使用与GID相同的数字UID。如果提供了用户名或组名，则容器的根文件系统 `/etc/passwd`和`/etc/group`文件将分别用于执行从名称到整数UID或GID的转换。以下示例显示了该`--chown`标志的有效定义：

```
COPY --chown=55:mygroup files* /somedir/
COPY --chown=bin files* /somedir/
COPY --chown=1 files* /somedir/
COPY --chown=10:11 files* /somedir/
```

如果容器根文件系统不包含任何文件`/etc/passwd`或 `/etc/group`文件，并且`--chown` 标志中使用了用户名或组名，则构建将在`COPY`操作上失败。使用数字ID不需要查找，也不依赖于容器根文件系统内容。

> **注意**：如果使用STDIN（`docker build - < somefile`）构建，则没有构建上下文，因此`COPY`无法使用。

（可选）`COPY`接受一个标志`--from=<name|index>`，该标志可用于将源位置设置为`FROM .. AS <name>`将用于替代用户发送的构建上下文的先前构建阶段（使用其创建）。该标志还接受为`FROM`指令启动的所有先前构建阶段分配的数字索引 。如果找不到具有指定名称的构建阶段，则尝试使用具有相同名称的镜像。

`COPY` 遵守以下规则：

*   该`<src>`路径必须是内部*语境*的构建; 你不能`COPY ../something /something`，因为a的第一步 `docker build`是将上下文目录（和子目录）发送到docker守护程序。

*   如果`<src>`是目录，则复制目录的全部内容，包括文件系统元数据。

> **注意**：不复制目录本身，只复制其内容。

*   如果`<src>`是任何其他类型的文件，则将其与元数据一起单独复制。在这种情况下，如果`<dest>`以尾部斜杠结尾`/`，则将其视为目录，`<src>`并将写入内容`<dest>/base(<src>)`。

*   如果`<src>`直接或由于使用通配符指定了多个资源，则`<dest>`必须是目录，并且必须以斜杠结尾`/`。

*   如果`<dest>`不以尾部斜杠结束，则将其视为常规文件，`<src>`并将写入其中的内容`<dest>`。

*   如果`<dest>`不存在，则会在其路径中创建所有缺少的目录。

## ENTRYPOINT

ENTRYPOINT有两种形式：

*   `ENTRYPOINT ["executable", "param1", "param2"]` （*执行*形式，首选）
*   `ENTRYPOINT command param1 param2` （*贝壳*形式）

An `ENTRYPOINT`允许您配置将作为可执行文件运行的容器。

例如，以下将使用其默认内容启动nginx，侦听端口80：

```
docker run -i -t --rm -p 80:80 nginx
```

命令行参数`docker run <image>`将附加在*exec*表单中的所有元素之后`ENTRYPOINT`，并将覆盖使用指定的所有元素`CMD`。这允许将参数传递给入口点，`docker run <image> -d` 即将`-d`参数传递给入口点。您可以`ENTRYPOINT`使用`docker run --entrypoint` 标志覆盖指令。

所述*壳*形式防止任何`CMD`或`run`被使用命令行参数，但是具有你的缺点`ENTRYPOINT`将被开始作为一个子命令`/bin/sh -c`，其不通过信号。这意味着可执行文件将不是容器`PID 1`- 并且*不会*收到Unix信号 - 因此您的可执行文件将不会收到 `SIGTERM`来自`docker stop <container>`。

只有意志中的最后一条`ENTRYPOINT`指令`Dockerfile`才有效。

### Exec形成ENTRYPOINT示例

您可以使用*exec*形式`ENTRYPOINT`设置相当稳定的默认命令和参数，然后使用任一形式`CMD`设置更可能更改的其他默认值。

```
FROM ubuntu
ENTRYPOINT ["top", "-b"]
CMD ["-c"]

```

运行容器时，您可以看到这`top`是唯一的进程：

```
$ docker run -it --rm --name test  top -H
top - 08:25:00 up  7:27,  0 users,  load average: 0.00, 0.01, 0.05
Threads:   1 total,   1 running,   0 sleeping,   0 stopped,   0 zombie
%Cpu(s):  0.1 us,  0.1 sy,  0.0 ni, 99.7 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
KiB Mem:   2056668 total,  1616832 used,   439836 free,    99352 buffers
KiB Swap:  1441840 total,        0 used,  1441840 free.  1324440 cached Mem

  PID USER      PR  NI    VIRT    RES    SHR S %CPU %MEM     TIME+ COMMAND
    1 root      20   0   19744   2336   2080 R  0.0  0.1   0:00.04 top

```

要进一步检查结果，您可以使用`docker exec`：

```
$ docker exec -it test ps aux
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  2.6  0.1  19752  2352 ?        Ss+  08:24   0:00 top -b -H
root         7  0.0  0.1  15572  2164 ?        R+   08:25   0:00 ps aux

```

并且您可以优雅地请求`top`关闭使用`docker stop test`。

以下`Dockerfile`显示使用`ENTRYPOINT`在前台运行Apache（即as `PID 1`）：

```
FROM debian:stable
RUN apt-get update && apt-get install -y --force-yes apache2
EXPOSE 80 443
VOLUME ["/var/www", "/var/log/apache2", "/etc/apache2"]
ENTRYPOINT ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]

```

如果需要为单个可执行文件编写启动脚本，可以使用`exec`和`gosu` 命令确保最终的可执行文件接收Unix信号：

```
#!/usr/bin/env bash
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

最后，如果您需要在关机时进行一些额外的清理（或与其他容器通信），或者协调多个可执行文件，您可能需要确保`ENTRYPOINT`脚本接收Unix信号，传递它们，然后执行一些更多的工作：

```
#!/bin/sh
# Note: I've written this using sh so it works in the busybox container too

# USE the trap if you need to also do manual cleanup after the service is stopped,
#     or need to start multiple services in the one container
trap "echo TRAPed signal" HUP INT QUIT TERM

# start service in background here
/usr/sbin/apachectl start

echo "[hit enter key to exit] or run 'docker stop <container>'"
read

# stop service and clean up here
echo "stopping apache"
/usr/sbin/apachectl stop

echo "exited $0"

```

如果运行此镜像`docker run -it --rm -p 80:80 --name test apache`，则可以使用`docker exec`，或检查容器的进程`docker top`，然后请求脚本停止Apache：

```
$ docker exec -it test ps aux
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.1  0.0   4448   692 ?        Ss+  00:42   0:00 /bin/sh /run.sh 123 cmd cmd2
root        19  0.0  0.2  71304  4440 ?        Ss   00:42   0:00 /usr/sbin/apache2 -k start
www-data    20  0.2  0.2 360468  6004 ?        Sl   00:42   0:00 /usr/sbin/apache2 -k start
www-data    21  0.2  0.2 360468  6000 ?        Sl   00:42   0:00 /usr/sbin/apache2 -k start
root        81  0.0  0.1  15572  2140 ?        R+   00:44   0:00 ps aux
$ docker top test
PID                 USER                COMMAND
10035               root                {run.sh} /bin/sh /run.sh 123 cmd cmd2
10054               root                /usr/sbin/apache2 -k start
10055               33                  /usr/sbin/apache2 -k start
10056               33                  /usr/sbin/apache2 -k start
$ /usr/bin/time docker stop test
test
real	0m 0.27s
user	0m 0.03s
sys	0m 0.03s

```

> **注意：**您可以使用覆盖`ENTRYPOINT`设置`--entrypoint`，但这只能将二进制设置为*exec*（不会`sh -c`使用）。

> **注意**：*exec*表单被解析为JSON数组，这意味着您必须使用双引号（“）来围绕单词而不是单引号（'）。

> **注意**：与*shell*表单不同，*exec*表单不会调用命令shell。这意味着不会发生正常的shell处理。例如， `ENTRYPOINT [ "echo", "$HOME" ]`不会对变量进行替换`$HOME`。如果你想要shell处理，那么要么使用*shell*表单，要么直接执行shell，例如：`ENTRYPOINT [ "sh", "-c", "echo $HOME" ]`。当使用exec表单并直接执行shell时，就像shell表单的情况一样，它是执行环境变量扩展的shell，而不是docker。

### Shell表格ENTRYPOINT示例

您可以为`ENTRYPOINT`它指定一个纯字符串，它将在其中执行`/bin/sh -c`。此表单将使用shell处理来替换shell环境变量，并将忽略任何`CMD`或`docker run`命令行参数。为了确保能够正确地`docker stop`发出任何长时间运行的`ENTRYPOINT`可执行文件，您需要记住启动它`exec`：

```
FROM ubuntu
ENTRYPOINT exec top -b

```

运行此镜像时，您将看到单个`PID 1`进程：

```
$ docker run -it --rm --name test top
Mem: 1704520K used, 352148K free, 0K shrd, 0K buff, 140368121167873K cached
CPU:   5% usr   0% sys   0% nic  94% idle   0% io   0% irq   0% sirq
Load average: 0.08 0.03 0.05 2/98 6
  PID  PPID USER     STAT   VSZ %VSZ %CPU COMMAND
    1     0 root     R     3164   0%   0% top -b

```

哪个将彻底退出`docker stop`：

```
$ /usr/bin/time docker stop test
test
real	0m 0.20s
user	0m 0.02s
sys	0m 0.04s

```

如果您忘记添加`exec`到您的开头`ENTRYPOINT`：

```
FROM ubuntu
ENTRYPOINT top -b
CMD --ignored-param1

```

然后，您可以运行它（为下一步命名）：

```
$ docker run -it --name test top --ignored-param2
Mem: 1704184K used, 352484K free, 0K shrd, 0K buff, 140621524238337K cached
CPU:   9% usr   2% sys   0% nic  88% idle   0% io   0% irq   0% sirq
Load average: 0.01 0.02 0.05 2/101 7
  PID  PPID USER     STAT   VSZ %VSZ %CPU COMMAND
    1     0 root     S     3168   0%   0% /bin/sh -c top -b cmd cmd2
    7     1 root     R     3164   0%   0% top -b

```

您可以从输出中`top`看到指定`ENTRYPOINT`的不是`PID 1`。

如果然后运行`docker stop test`，容器将不会干净地退出 - `stop`命令将被强制`SIGKILL`在超时后发送：

```
$ docker exec -it test ps aux
PID   USER     COMMAND
    1 root     /bin/sh -c top -b cmd cmd2
    7 root     top -b
    8 root     ps aux
$ /usr/bin/time docker stop test
test
real	0m 10.19s
user	0m 0.04s
sys	0m 0.03s

```

### 了解CMD和ENTRYPOINT如何相互作用

Both `CMD`和`ENTRYPOINT`instructions指定运行容器时执行的命令。很少有规则描述他们的合作。

1.  Dockerfile应至少指定一个`CMD`或`ENTRYPOINT`命令。

2.  `ENTRYPOINT` 应该在将容器用作可执行文件时定义。

3.  `CMD`应该用作定义`ENTRYPOINT`命令的默认参数或在容器中执行ad-hoc命令的方法。

4.  `CMD` 在使用替代参数运行容器时将被覆盖。

下表显示了针对不同`ENTRYPOINT`/ `CMD`组合执行的命令：

|   | 没有ENTRYPOINT | ENTRYPOINT exec_entry p1_entry | ENTRYPOINT [“exec_entry”，“p1_entry”] |
| --- | --- | --- | --- |
| **没有CMD** | *错误，不允许* | / bin / sh -c exec_entry p1_entry | exec_entry p1_entry |
| **CMD [“exec_cmd”，“p1_cmd”]** | exec_cmd p1_cmd | / bin / sh -c exec_entry p1_entry | exec_entry p1_entry exec_cmd p1_cmd |
| **CMD [“p1_cmd”，“p2_cmd”]** | p1_cmd p2_cmd | / bin / sh -c exec_entry p1_entry | exec_entry p1_entry p1_cmd p2_cmd |
| **CMD exec_cmd p1_cmd** | / bin / sh -c exec_cmd p1_cmd | / bin / sh -c exec_entry p1_entry | exec_entry p1_entry / bin / sh -c exec_cmd p1_cmd |

## 卷

```
VOLUME ["/data"]

```

该`VOLUME`指令创建具有指定名称的安装点，并将其标记为从本机主机或其他容器保存外部安装的卷。该值可以是JSON数组，`VOLUME ["/var/log/"]`或具有多个参数的普通字符串，例如`VOLUME /var/log`或`VOLUME /var/log /var/db`。有关通过Docker客户端提供的更多信息/示例和安装说明，请参阅 [*通过卷共享目录*](https://docs.docker.com/engine/tutorials/dockervolumes/#/mount-a-host-directory-as-a-data-volume) 文档。

该`docker run`命令使用基础镜像中指定位置存在的任何数据初始化新创建的卷。例如，请考虑以下Dockerfile片段：

```
FROM ubuntu
RUN mkdir /myvol
RUN echo "hello world" > /myvol/greeting
VOLUME /myvol

```

此Dockerfile会`docker run`生成一个镜像，该镜像将导致创建新的挂载点`/myvol`并将`greeting`文件复制 到新创建的卷中。

### 有关指定卷的说明

关于卷中的卷，请记住以下事项`Dockerfile`。

*   **基于Windows的容器上的卷**：使用基于Windows的容器时，容器中卷的目标必须是以下之一：

    *   不存在或空目录
    *   除了之外的驱动器 `C:`
*   **从Dockerfile中更改卷**：如果任何构建步骤在声明后**更改卷内的**数据，那么这些更改将被丢弃。

*   **JSON格式**：列表被解析为JSON数组。您必须用双引号（`"`）而不是单引号（`'`）括起单词。

*   **主机目录在容器运行时声明**：主机目录（mountpoint）本质上是依赖于主机的。这是为了保持镜像的可移植性，因为不能保证给定的主机目录在所有主机上都可用。因此，您无法从Dockerfile中安装主机目录。该`VOLUME`指令不支持指定`host-dir` 参数。您必须在创建或运行容器时指定安装点。

## 用户

```
USER <user>[:<group>] or
USER <UID>[:<GID>]

```

的`USER`运行的镜像和用于当任何指令设置的用户名（或UID）和任选的所述用户组（或GID）使用`RUN`，`CMD`和 `ENTRYPOINT`它后面的指令`Dockerfile`。

> **警告**：当用户没有主要组时，镜像（或下一个说明）将与该`root`组一起运行。

> 在Windows上，如果用户不是内置帐户，则必须先创建用户。这可以通过`net user`作为Dockerfile的一部分调用的命令来完成。

```
    FROM microsoft/windowsservercore
    # Create Windows user in the container
    RUN net user /add patrick
    # Set it for subsequent commands
    USER patrick

```

## WORKDIR

```
WORKDIR /path/to/workdir

```

该`WORKDIR`指令集的工作目录对任何`RUN`，`CMD`， `ENTRYPOINT`，`COPY`和`ADD`它后面的说明`Dockerfile`。如果`WORKDIR`不存在，即使它未在任何后续`Dockerfile`指令中使用，也将创建它。

该`WORKDIR`指令可以在a中多次使用`Dockerfile`。如果提供了相对路径，则它将相对于前一条`WORKDIR`指令的路径 。例如：

```
WORKDIR /a
WORKDIR b
WORKDIR c
RUN pwd

```

最终`pwd`命令的输出`Dockerfile`将是 `/a/b/c`。

该`WORKDIR`指令可以解析先前使用的环境变量 `ENV`。您只能使用显式设置的环境变量`Dockerfile`。例如：

```
ENV DIRPATH /path
WORKDIR $DIRPATH/$DIRNAME
RUN pwd

```

最终`pwd`命令的输出`Dockerfile`将是 `/path/$DIRNAME`

## ARG

```
ARG <name>[=<default value>]

```

该`ARG`指令定义了一个变量，用户可以`docker build`使用该`--build-arg <varname>=<value>`标志在构建时将该变量传递给构建器。如果用户指定了未在Dockerfile中定义的构建参数，则构建会输出警告。

```
[Warning] One or more build-args [foo] were not consumed.

```

Dockerfile可以包括一个或多个`ARG`指令。例如，以下是有效的Dockerfile：

```
FROM busybox
ARG user1
ARG buildno
...

```

> **警告：**建议不要使用构建时变量来传递密码，例如github密钥，用户凭据等`docker history`。使用该命令，构建时变量值对于镜像的任何用户都是可见的。

### 默认值

的`ARG`指令可以可选地包括一个默认值：

```
FROM busybox
ARG user1=someuser
ARG buildno=1
...

```

如果`ARG`指令具有默认值，并且在构建时没有传递值，则构建器将使用默认值。

### 范围

一个`ARG`变量定义进入从在其上在限定的线效果`Dockerfile`不从参数对命令行或其他地方使用。例如，考虑这个Dockerfile：

```
1 FROM busybox
2 USER ${user:-some_user}
3 ARG user
4 USER $user
...

```

用户通过调用以下内容构建此文件：

```
$ docker build --build-arg user=what_user .

```

第`USER`2行计算`some_user`为`user`变量在后续第3行定义。第`USER`4行计算结果`what_user`为`user`定义，并`what_user`在命令行上传递值。在通过`ARG`指令定义之前 ，对变量的任何使用都会导致空字符串。

一个`ARG`指令超出范围在它被定义的构建阶段结束。要在多个阶段中使用arg，每个阶段都必须包含该`ARG`指令。

```
FROM busybox
ARG SETTINGS
RUN ./run/setup $SETTINGS

FROM busybox
ARG SETTINGS
RUN ./run/other $SETTINGS

```

### 使用ARG变量

您可以使用`ARG`或`ENV`指令指定指令可用的变量`RUN`。使用该`ENV`指令定义的环境变量 始终覆盖`ARG`同名指令。考虑这个Dockerfile和一个`ENV`和`ARG`指令。

```
1 FROM ubuntu
2 ARG CONT_IMG_VER
3 ENV CONT_IMG_VER v1.0.0
4 RUN echo $CONT_IMG_VER

```

然后，假设使用此命令构建此镜像：

```
$ docker build --build-arg CONT_IMG_VER=v2.0.1 .

```

在这种情况下，`RUN`指令使用`v1.0.0`而不是`ARG`用户传递的设置：`v2.0.1`此行为类似于shell脚本，其中本地范围的变量覆盖作为参数传递的变量或从其定义的环境继承的变量。

使用上面的示例但不同的`ENV`规范，您可以在指令`ARG`和`ENV`指令之间创建更有用的交互：

```
1 FROM ubuntu
2 ARG CONT_IMG_VER
3 ENV CONT_IMG_VER ${CONT_IMG_VER:-v1.0.0}
4 RUN echo $CONT_IMG_VER

```

与`ARG`指令不同，`ENV`值始终保留在构建的镜像中。考虑没有`--build-arg`标志的docker构建：

```
$ docker build .

```

使用此Dockerfile示例`CONT_IMG_VER`仍然保留在镜像中，但其值将`v1.0.0`与`ENV`指令中第3行的默认值相同。

此示例中的变量扩展技术允许您从命令行传递参数，并通过利用该`ENV`指令将它们保留在最终镜像中 。只有[一组有限的Dockerfile指令](https://docs.docker.com/engine/reference/builder/#environment-replacement)支持变量扩展[。](https://docs.docker.com/engine/reference/builder/#environment-replacement)

### 预定义的ARG

Docker有一组预定义`ARG`变量，您可以`ARG`在Dockerfile中使用相应的指令。

*   `HTTP_PROXY`
*   `http_proxy`
*   `HTTPS_PROXY`
*   `https_proxy`
*   `FTP_PROXY`
*   `ftp_proxy`
*   `NO_PROXY`
*   `no_proxy`

要使用它们，只需使用标志在命令行上传递它们：

```
--build-arg <varname>=<value>

```

默认情况下，这些预定义变量将从输出中排除 `docker history`。排除它们可以降低在`HTTP_PROXY`变量中意外泄露敏感验证信息的风险。

例如，考虑使用构建以下Dockerfile`--build-arg HTTP_PROXY=http://user:pass@proxy.lon.example.com`

```
FROM ubuntu
RUN echo "Hello World"

```

在这种情况下，`HTTP_PROXY`变量的值在`docker history`和中不可用， 并且不会被缓存。如果您要更改位置，并且您的代理服务器已更改为`http://user:pass@proxy.sfo.example.com`，则后续构建不会导致缓存未命中。

如果需要覆盖此行为，则可以通过`ARG` 在Dockerfile中添加语句来执行此操作，如下所示：

```
FROM ubuntu
ARG HTTP_PROXY
RUN echo "Hello World"

```

构建此Dockerfile时，`HTTP_PROXY`会保留在其中 `docker history`，并且更改其值会使构建缓存无效。

### 对构建缓存的影响

`ARG`变量不会像`ENV`变量那样持久保存在构建的镜像中。但是，`ARG`变量确实以类似的方式影响构建缓存。如果Dockerfile定义了一个`ARG`值与前一个版本不同的变量，则在第一次使用时会发生“缓存未命中”，而不是其定义。特别是，`RUN`指令后面的所有指令都 隐式`ARG`使用`ARG`变量（作为环境变量），因此可能导致高速缓存未命中。`ARG`除非在中包含匹配的`ARG`语句，否则所有预定义变量都将免于缓存`Dockerfile`。

例如，考虑这两个Dockerfile：

```
1 FROM ubuntu
2 ARG CONT_IMG_VER
3 RUN echo $CONT_IMG_VER

```

```
1 FROM ubuntu
2 ARG CONT_IMG_VER
3 RUN echo hello

```

如果`--build-arg CONT_IMG_VER=<value>`在命令行中指定，则在两种情况下，第2行上的规范都不会导致高速缓存未命中; 第3行确实导致缓存未命中。`ARG CONT_IMG_VER`导致RUN行被识别为与运行`CONT_IMG_VER=<value>`echo hello 相同，因此如果`<value>` 更改，我们将获得缓存未命中。

考虑同一命令行下的另一个示例：

```
1 FROM ubuntu
2 ARG CONT_IMG_VER
3 ENV CONT_IMG_VER $CONT_IMG_VER
4 RUN echo $CONT_IMG_VER

```

在此示例中，高速缓存未命中发生在第3行。发生未命中是因为`ENV`引用`ARG`变量的变量值和通过命令行更改了该变量。在此示例中，该`ENV` 命令使镜像包含该值。

如果一条`ENV`指令覆盖了一个`ARG`同名的指令，比如这个Dockerfile：

```
1 FROM ubuntu
2 ARG CONT_IMG_VER
3 ENV CONT_IMG_VER hello
4 RUN echo $CONT_IMG_VER

```

第3行不会导致缓存未命中，因为值为`CONT_IMG_VER`常量（`hello`）。因此，`RUN`（第4行）上使用的环境变量和值在构建之间不会发生变化。

## ONBUILD

```
ONBUILD [INSTRUCTION]

```

当镜像用作另一个构建的基础时，该`ONBUILD`指令向镜像添加将在稍后执行的*触发*指令。触发器将在下游构建的上下文中执行，就好像它已经`FROM`在下游指令之后立即插入一样 `Dockerfile`。

任何构建指令都可以注册为触发器。

如果要构建将用作构建其他镜像的基础的镜像（例如，可以使用特定于用户的配置自定义的应用程序构建环境或守护程序），这将非常有用。

例如，如果您的镜像是可重用的Python应用程序构建器，则需要将应用程序源代码添加到特定目录中，并且可能需要*在* 此*之后*调用构建脚本。你不能只是打电话`ADD`和`RUN`现在，因为你还没有访问应用程序的源代码，这将是为每个应用程序生成不同的。您可以简单地为应用程序开发人员提供`Dockerfile`复制粘贴到他们的应用程序中的样板，但这样做效率低，容易出错且难以更新，因为它与特定于应用程序的代码混合在一起。

解决方案是用于`ONBUILD`在下一个构建阶段注册预先指令以便稍后运行。

以下是它的工作原理：

1.  当遇到`ONBUILD`指令时，构建器会向正在构建的镜像的元数据添加触发器。该指令不会影响当前构建。
2.  在构建结束时，所有触发器的列表存储在键下的镜像清单中`OnBuild`。可以使用该`docker inspect`命令检查它们。
3.  稍后，可以使用该`FROM`指令将镜像用作新构建的基础 。作为处理`FROM`指令的一部分，下游构建器查找`ONBUILD`触发器，并按照它们注册的顺序执行它们。如果任何触发器失败，`FROM`则中止指令，这反过来导致构建失败。如果所有触发器都成功，则`FROM`指令完成并且构建继续照常进行。
4.  执行后，触发器将从最终镜像中清除。换句话说，它们不是由“大孩子”构建继承的。

例如，您可以添加以下内容：

```
[...]
ONBUILD ADD . /app/src
ONBUILD RUN /usr/local/bin/python-build --dir /app/src
[...]

```

> **警告**：不允许`ONBUILD`使用链接指令`ONBUILD ONBUILD`。

> **警告**：`ONBUILD`指令可能不会触发`FROM`或`MAINTAINER`指令。

## STOPSIGNAL

```
STOPSIGNAL signal

```

该`STOPSIGNAL`指令设置将发送到容器的系统调用信号以退出。此信号可以是与内核的系统调用表中的位置匹配的有效无符号数，例如9，或SIGNAME格式的信号名，例如SIGKILL。

## 健康检查

该`HEALTHCHECK`指令有两种形式：

*   `HEALTHCHECK [OPTIONS] CMD command` （通过在容器内运行命令来检查容器运行状况）
*   `HEALTHCHECK NONE` （禁用从基础镜像继承的任何运行状况检查）

该`HEALTHCHECK`指令告诉Docker如何测试容器以检查它是否仍在工作。即使服务器进程仍在运行，这也可以检测到陷入无限循环且无法处理新连接的Web服务器等情况。

当容器指定了*运行状况检查时*，除了正常状态外，它还具有*运行*状况。这个状态最初是`starting`。每当健康检查通过时，它就会变成`healthy`（以前的状态）。经过一定数量的连续失败后，它就变成了`unhealthy`。

之前可以出现的选项`CMD`是：

*   `--interval=DURATION`（默认值：`30s`）
*   `--timeout=DURATION`（默认值：`30s`）
*   `--start-period=DURATION`（默认值：`0s`）
*   `--retries=N`（默认值：`3`）

运行状况检查将首先在容器启动后的**间隔**秒运行，然后在每次上一次检查完成后再**间隔**秒。

如果单次运行的检查花费的时间超过**超时**秒数，那么检查将被视为失败。

它需要**重试**连续的健康检查失败才能考虑容器`unhealthy`。

**start period**为需要时间引导的容器提供初始化时间。在此期间探测失败将不计入最大重试次数。但是，如果在启动期间运行状况检查成功，则会将容器视为已启动，并且所有连续失败将计入最大重试次数。

`HEALTHCHECK`Dockerfile中只能有一条指令。如果列出多个，则只有最后一个`HEALTHCHECK`生效。

`CMD`关键字后面的命令可以是shell命令（例如`HEALTHCHECK CMD /bin/check-running`）或*exec*数组（与其他Dockerfile命令一样; `ENTRYPOINT`有关详细信息，请参阅参考资料）。

命令的退出状态指示容器的运行状况。可能的值是：

*   0：成功 - 容器健康且随时可用
*   1：不健康 - 容器无法正常工作
*   2：保留 - 不要使用此退出代码

例如，要检查每五分钟左右网络服务器能够在三秒钟内为网站的主页面提供服务：

```
HEALTHCHECK --interval=5m --timeout=3s \
  CMD curl -f http://localhost/ || exit 1

```

为了帮助调试失败的探测器，命令在stdout或stderr上写入的任何输出文本（UTF-8编码）将存储在运行状况中并可以使用查询 `docker inspect`。此类输出应保持较短（目前仅存储前4096个字节）。

当容器的运行状况更改时，将`health_status`生成具有新状态的事件。

该`HEALTHCHECK`功能已添加到Docker 1.12中。

## 贝壳

```
SHELL ["executable", "parameters"]

```

该`SHELL`指令允许覆盖用于*shell*形式的命令的默认shell 。Linux上的默认shell是`["/bin/sh", "-c"]`，而在Windows上`["cmd", "/S", "/C"]`。该`SHELL`指令*必须*以JSON格式写入Dockerfile。

的`SHELL`：其中有两个常用的和完全不同的原生贝壳指令是在Windows上特别有用`cmd`和`powershell`，以及提供包括候补炮弹`sh`。

该`SHELL`指令可以多次出现。每条`SHELL`指令都会覆盖所有先前的`SHELL`指令，并影响所有后续指令。例如：

```
FROM microsoft/windowsservercore

# Executed as cmd /S /C echo default
RUN echo default

# Executed as cmd /S /C powershell -command Write-Host default
RUN powershell -command Write-Host default

# Executed as powershell -command Write-Host hello
SHELL ["powershell", "-command"]
RUN Write-Host hello

# Executed as cmd /S /C echo hello
SHELL ["cmd", "/S", "/C"]
RUN echo hello

```

以下说明可以通过影响`SHELL`指令时， *壳*他们的形式在一个Dockerfile使用：`RUN`，`CMD`和`ENTRYPOINT`。

以下示例是在Windows上找到的常见模式，可以使用以下`SHELL`指令简化：

```
...
RUN powershell -command Execute-MyCmdlet -param1 "c:\foo.txt"
...

```

docker调用的命令将是：

```
cmd /S /C powershell -command Execute-MyCmdlet -param1 "c:\foo.txt"

```

由于两个原因，这是低效的。首先，调用一个不必要的cmd.exe命令处理器（也就是shell）。其次，*shell* 形式的每条`RUN`指令都需要额外的命令前缀。`powershell -command`

为了提高效率，可以采用两种机制中的一种。一种是使用RUN命令的JSON形式，例如：

```
...
RUN ["powershell", "-command", "Execute-MyCmdlet", "-param1 \"c:\\foo.txt\""]
...

```

虽然JSON表单是明确的，并且不使用不必要的cmd.exe，但它确实需要通过双引号和转义更加详细。替代机制是使用`SHELL`指令和*shell*表单，为Windows用户创建更自然的语法，尤其是与`escape`解析器指令结合使用时：

```
# escape=`

FROM microsoft/nanoserver
SHELL ["powershell","-command"]
RUN New-Item -ItemType Directory C:\Example
ADD Execute-MyCmdlet.ps1 c:\example\
RUN c:\example\Execute-MyCmdlet -sample 'hello world'

```

导致：

```
PS E:\docker\build\shell> docker build -t shell .
Sending build context to Docker daemon 4.096 kB
Step 1/5 : FROM microsoft/nanoserver
 ---> 22738ff49c6d
Step 2/5 : SHELL powershell -command
 ---> Running in 6fcdb6855ae2
 ---> 6331462d4300
Removing intermediate container 6fcdb6855ae2
Step 3/5 : RUN New-Item -ItemType Directory C:\Example
 ---> Running in d0eef8386e97

    Directory: C:\

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----       10/28/2016  11:26 AM                Example

 ---> 3f2fbf1395d9
Removing intermediate container d0eef8386e97
Step 4/5 : ADD Execute-MyCmdlet.ps1 c:\example\
 ---> a955b2621c31
Removing intermediate container b825593d39fc
Step 5/5 : RUN c:\example\Execute-MyCmdlet 'hello world'
 ---> Running in be6d8e63fe75
hello world
 ---> 8e559e9bf424
Removing intermediate container be6d8e63fe75
Successfully built 8e559e9bf424
PS E:\docker\build\shell>

```

该`SHELL`指令还可用于修改shell的运行方式。例如，`SHELL cmd /S /C /V:ON|OFF`在Windows上使用，可以修改延迟的环境变量扩展语义。

的`SHELL`，也可以在Linux上使用的指令应当替代壳需要如`zsh`，`csh`，`tcsh`和其他。

该`SHELL`功能已添加到Docker 1.12中。

## Dockerfile示例

下面您可以看到Dockerfile语法的一些示例。如果您对更现实的东西感兴趣，请查看[Docker化示例](https://docs.docker.com/engine/examples/)列表。

```
# Nginx
#
# VERSION               0.0.1

FROM      ubuntu
LABEL Description="This image is used to start the foobar executable" Vendor="ACME Products" Version="1.0"
RUN apt-get update && apt-get install -y inotify-tools nginx apache2 openssh-server

```

```
# Firefox over VNC
#
# VERSION               0.3

FROM ubuntu

# Install vnc, xvfb in order to create a 'fake' display and firefox
RUN apt-get update && apt-get install -y x11vnc xvfb firefox
RUN mkdir ~/.vnc
# Setup a password
RUN x11vnc -storepasswd 1234 ~/.vnc/passwd
# Autostart firefox (might not be the best way, but it does the trick)
RUN bash -c 'echo "firefox" >> /.bashrc'

EXPOSE 5900
CMD    ["x11vnc", "-forever", "-usepw", "-create"]

```

```
# Multiple images example
#
# VERSION               0.1

FROM ubuntu
RUN echo foo > bar
# Will output something like ===> 907ad6c2736f

FROM ubuntu
RUN echo moo > oink
# Will output something like ===> 695d7793cbe4

# You'll now have two images, 907ad6c2736f with /bar, and 695d7793cbe4 with
# /oink.

```

[建设者](https://docs.docker.com/glossary/?term=builder)，[搬运工](https://docs.docker.com/glossary/?term=docker)，[Dockerfile](https://docs.docker.com/glossary/?term=Dockerfile)，[自动化](https://docs.docker.com/glossary/?term=automation)，[镜像创作](https://docs.docker.com/glossary/?term=image%20creation)
