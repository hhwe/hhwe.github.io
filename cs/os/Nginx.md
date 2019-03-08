[启动，停止和重新加载配置](http://nginx.org/en/docs/beginners_guide.html#control)
[配置文件的结构](http://nginx.org/en/docs/beginners_guide.html#conf_structure)
[服务静态内容](http://nginx.org/en/docs/beginners_guide.html#static)
[设置简单代理服务器](http://nginx.org/en/docs/beginners_guide.html#proxy)
[设置FastCGI代理](http://nginx.org/en/docs/beginners_guide.html#fastcgi)

本指南提供了对nginx的基本介绍，并介绍了可以使用它完成的一些简单任务，请确保nginx已安装，如果不是，请参阅[安装nginx](http://nginx.org/en/docs/install.html)页面。本指南介绍如何启动和停止nginx，重新加载其配置，解释配置文件的结构，并介绍如何设置nginx以提供静态内容，如何将nginx配置为代理服务器，以及如何将其与一个FastCGI应用程序。

nginx有一个主进程和几个工作进程。主进程的主要目的是读取和评估配置，并维护工作进程。工作进程会对请求进行实际处理。nginx使用基于事件的模型和依赖于操作系统的机制来有效地在工作进程之间分发请求。工作进程数在配置文件中定义，可以针对给定配置进行修复，也可以自动调整为可用CPU内核数（请参阅[worker_processes](http://nginx.org/en/docs/ngx_core_module.html#worker_processes)）。

> nginx及其模块的工作方式在配置文件中确定。默认情况下，配置文件被命名`nginx.conf` 并放在目录`/usr/local/nginx/conf`中 `/etc/nginx`，或 `/usr/local/etc/nginx`。

## 启动，停止和重新加载配置

要启动nginx，请运行可执行文件。启动nginx后，可以通过使用`-s`参数调用可执行文件来控制它。使用以下语法：

```
nginx -s signal
```

*信号*可以是下列之一：

*   `stop` - 快速关机
*   `quit` - 优雅的关机
*   `reload` - 重新加载配置文件
*   `reopen` - 重新打开日志文件

例如，要在等待工作进程完成当前请求的服务时停止nginx进程，可以执行以下命令：

```
nginx -s quit
```

> 此命令应在启动nginx的同一用户下执行。

在将重新加载配置的命令发送到nginx或重新启动之前，将不会应用配置文件中所做的更改。要重新加载配置，请执行：

```
nginx -s reload
```

一旦主进程收到重新加载配置的信号，它将检查新配置文件的语法有效性并尝试应用其中提供的配置。如果成功，主进程将启动新的工作进程并向旧工作进程发送消息，请求它们关闭。否则，主进程将回滚更改并继续使用旧配置。旧工作进程，接收命令关闭，停止接受新连接并继续为当前请求提供服务，直到所有此类请求都得到服务。之后，旧工作进程退出。

也可以借助Unix工具（如`kill`实用程序）将信号发送到nginx进程。在这种情况下，信号直接发送到具有给定进程ID的进程。默认情况下，nginx主进程的进程ID写入 `nginx.pid`目录 `/usr/local/nginx/logs`或 `/var/run`。例如，如果主进程ID是1628，要发送导致nginx正常关闭的QUIT信号，请执行：

```
kill -s QUIT 1628
```

要获取所有正在运行的nginx进程的列表，`ps` 可以使用该实用程序，例如，通过以下方式：

```
ps -ax | grep nginx
```

有关向nginx发送信号的更多信息，请参阅 [控制nginx](http://nginx.org/en/docs/control.html)。

## 配置文件的结构

nginx由模块组成，这些模块由配置文件中指定的指令控制。指令分为简单指令和块指令。一个简单的指令包括由空格分隔的名称和参数，以分号（`;`）结尾。块指令与简单指令具有相同的结构，但它不是以分号结尾，而是以大括号（`{`和`}`）包围的一组附加指令结束。如果块指令可以在大括号内包含其他指令，则称为上下文（示例： [events](http://nginx.org/en/docs/ngx_core_module.html#events)， [http](http://nginx.org/en/docs/http/ngx_http_core_module.html#http)， [server](http://nginx.org/en/docs/http/ngx_http_core_module.html#server)和 [location](http://nginx.org/en/docs/http/ngx_http_core_module.html#location)）。

放置在任何上下文之外的配置文件中的指令被认为是在 [主](http://nginx.org/en/docs/ngx_core_module.html)上下文中。在`events`和`http`指令驻留在`main`上下文`server` 中`http`，并`location`在 `server`。

`#`标志后面的其余部分被视为评论。

## 提供静态内容

一个重要的Web服务器任务是提供文件（例如图像或静态HTML页面）。您将实现一个示例，根据请求，将从不同的本地目录`/data/www` （可能包含HTML文件）和`/data/images` （包含图像）提供文件。这将需要编辑配置文件并需要在[server](http://nginx.org/en/docs/http/ngx_http_core_module.html#server)块的[http](http://nginx.org/en/docs/http/ngx_http_core_module.html#http)块内设置两个[location](http://nginx.org/en/docs/http/ngx_http_core_module.html#location) 块 。[](http://nginx.org/en/docs/http/ngx_http_core_module.html#http)[](http://nginx.org/en/docs/http/ngx_http_core_module.html#location)

首先，创建`/data/www`目录并将`index.html`包含任何文本内容的 文件放入其中，然后创建`/data/images`目录并在其中放置一些图像。

接下来，打开配置文件。默认配置文件已经包含了几个`server`块的示例，主要是注释掉了。现在注释掉所有这些块并开始一个新 `server`块：

```
http { 
    server { 

    }  
}
```

通常，配置文件可以包括由它们[listen](http://nginx.org/en/docs/http/ngx_http_core_module.html#listen)的端口和 [server names](http://nginx.org/en/docs/http/server_names.html)来[区分](http://nginx.org/en/docs/http/request_processing.html)的若干 `server`块 。一旦nginx决定对请求进行处理，它就会根据块内定义的指令 参数测试请求头中指定的URI 。 [](http://nginx.org/en/docs/http/request_processing.html)[](http://nginx.org/en/docs/http/ngx_http_core_module.html#listen)[](http://nginx.org/en/docs/http/server_names.html)`server``location``server`

将以下`location`块添加到 `server`块中：

```
location / { 
    root /data/www;
}
```

此`location`块指定`/`前缀与请求中的URI进行比较的。对于匹配请求，URI将添加到[root](http://nginx.org/en/docs/http/ngx_http_core_module.html#root) 指令中指定的路径 ，即to `/data/www`，以形成本地文件系统上所请求文件的路径。如果存在多个匹配`location`块，则nginx选择具有最长前缀的块。`location`上面的块提供长度为1的最短前缀，因此只有当所有其他`location` 块都无法提供匹配时，才会使用此块。

接下来，添加第二个`location`块：

```
location /images/ {
    root /data;
}
```

它将匹配以`/images/` 开头的请求（`location /`也匹配此类请求，但前缀更短）。

`server`块 的结果配置应如下所示：

```
server {
    location / {
        root /data/www;
    }

    location /images/ {
        root /data;
    }
}
```

这已经是服务器的工作配置，它可以侦听标准端口80，并且可以在本地计算机上访问 `http://localhost/`。为响应以`/images/`URI开头的请求，服务器将从`/data/images`目录发送文件。例如，响应`http://localhost/images/example.png`请求nginx将发送`/data/images/example.png`文件。如果此类文件不存在，nginx将发送指示404错误的响应。不以`/images/`URI开头的请求将映射到`/data/www`目录。例如，响应`http://localhost/some/example.html`请求nginx将发送`/data/www/some/example.html`文件。

要应用新配置，请启动nginx（如果尚未启动）或`reload`通过执行以下命令将信号发送到nginx的主进程：

```
nginx -s reload
```

> 在一些情况下不按预期工作，您可以尝试找出原因`access.log`和 `error.log`目录中的文件`/usr/local/nginx/logs`或 `/var/log/nginx`。

## 设置简单的代理服务器

nginx的一个常见用途是将其设置为代理服务器，这意味着服务器接收请求，将它们传递给代理服务器，从中检索响应，然后将它们发送给客户端。

我们将配置一个基本代理服务器，它使用来自本地目录的文件处理图像请求，并将所有其他请求发送到代理服务器。在此示例中，将在单个nginx实例上定义两个服务器。

首先，通过向`server` nginx的配置文件添加一个以上内容来定义代理服务器，其中包含以下内容：

```
server {
    listen 8080;
    root /data/up1;

    location / {
    }
}
```

这将是一个侦听端口8080的简单服务器（未指定`listen`指令之前，默认使用标准端口80）并将所有请求映射到`/data/up1`本地文件系统上的目录。创建此目录并将`index.html`文件放入其中。请注意，该`root`指令放在`server`上下文中。当选择用于提供请求的`location`块不包括自己的`root`指令时，使用这样的根指令。

接下来，使用上一节中的服务器配置并对其进行修改以使其成为代理服务器配置。在第一个`location`块中，将[proxy_pass](http://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_pass) 指令与参数中指定的代理服务器的协议，名称和端口放在一起（在我们的示例中，它是`http://localhost:8080`）：

```
server {
    location / {
        proxy_pass http://localhost:8080;
    }

    location /images/ {
        root /data;
    }
}
```

我们将修改第二个`location` 块，该块当前将带有`/images/` 前缀的请求映射到目录下的`/data/images`文件，以使其与具有典型文件扩展名的图像请求相匹配。修改后的`location`块看起来像这样：

```
location ~ \.(gif|jpg|png)$ {
    root /data/images;
}
```

该参数是一个正则表达式匹配结尾的所有URI `.gif`，`.jpg`或`.png`。应该以正则表达式开头`~`。相应的请求将映射到该`/data/images` 目录。

当nginx选择一个`location`块来提供请求时，它首先检查 指定前缀的[位置](http://nginx.org/en/docs/http/ngx_http_core_module.html#location)指令，记住`location` 最长的前缀，然后检查正则表达式。如果与正则表达式匹配，则nginx选择此项 `location`，否则，它会选择之前记住的那个。

生成的代理服务器配置如下所示：

```
server {
    location / {
        proxy_pass http://localhost:8080/;
    }

    location ~ \.(gif|jpg|png)$ {
        root /data/images;
    }
}
```

此服务器将过滤以`.gif`， `.jpg`或者`.png` 将其映射到`/data/images`目录的请求（通过向`root`指令的参数添加URI）并将所有其他请求传递给上面配置的代理服务器。

要应用新配置，请将`reload`信号发送到nginx，如前面部分所述。

更多[代理模块](http://nginx.org/en/docs/http/ngx_http_proxy_module.html) 可用于进一步配置代理服务器连接指令。

## 设置FastCGI代理

nginx可用于将请求路由到FastCGI服务器，这些服务器运行使用各种框架和编程语言（如PHP）构建的应用程序。

使用FastCGI服务器的最基本的nginx配置包括使用 [fastcgi_pass](http://nginx.org/en/docs/http/ngx_http_fastcgi_module.html#fastcgi_pass) 指令而不是`proxy_pass`指令，以及[fastcgi_param](http://nginx.org/en/docs/http/ngx_http_fastcgi_module.html#fastcgi_param) 指令来设置传递给FastCGI服务器的参数。假设可以访问FastCGI服务器`localhost:9000`。以上一节中的代理配置为基础，将`proxy_pass`指令替换为指令 `fastcgi_pass`并将参数更改为 `localhost:9000`。在PHP中，该`SCRIPT_FILENAME`参数用于确定脚本名称，该`QUERY_STRING` 参数用于传递请求参数。结果配置为：

```
server {
    location / {
        fastcgi_pass  localhost:9000;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        fastcgi_param QUERY_STRING    $query_string;
    }

    location ~ \.(gif|jpg|png)$ {
        root /data/images;
    }
}
```

这将设置一个服务器，该服务器将除静态图像请求之外的所有请求路由到`localhost:9000`通过FastCGI协议操作的代理服务器 。
