---
title: Let’s Build A Web Server
date: 2017-07-29 05:08:37
categories: Web
tags: 
    - python
    - HTTP
    - Web
---


本文是翻译至[Ruslan's Blog](https://ruslanspivak.com/)

主要介绍关于web服务器请求响应的主要流程和相关细节

本文分为三个部分，在这三部分系列中，我将向您展示如何构建您自己的基本Web服务器。让我们开始吧。

* [Part1](#1.0)：什么是`web server`
* [Part2](#2.0)：
* [Part3](#3.0)：


---

<h1 id="1.0">Part1</h1>


首先，什么是Web服务器？

![HTTP响应](images/2017-07-29/LSBAWS_HTTP_request_response.png)

简而言之，它是一个位于物理服务器（oops，服务器上的服务器）上的网络服务器，并等待客户端发送请求。当它收到请求时，会生成一个响应并将其发送回客户端。客户端和服务器之间的通信使用HTTP协议。客户端可以是您的浏览器或任何其他说HTTP的软件。

Web服务器的简单实现会是什么样的？下面是一个简单的websever代码：[webserver1.py](part1/webserver1.py)

在命令行上运行它

  $ python webserver1.py
  服务HTTP端口8888 ...

现在在Web浏览器的地址栏[http://localhost:8888/hello](http://localhost:8888/hello)中输入以下URL，点击Enter，并看到魔术在行动中。您的浏览器中应该会显示“Hello，World！”

只要这样做，认真。我会在你测试的时候等你。

完成了吗？好。现在我们来讨论一切如何运作。

首先让我们从您输入的网址开始。它被称为URL，这里是它的基本结构：

![网址结构](images/2017-07-29/LSBAWS_URL_Web_address.png)

这是您如何向浏览器发送需要查找和连接的Web服务器的地址以及服务器上的页面（路径），以便为您提取。在浏览器可以发送HTTP请求之前，首先需要与Web服务器建立TCP连接。然后它通过TCP连接向服务器发送HTTP请求，并等待服务器发回HTTP响应。当您的浏览器收到响应时，显示它，在这种情况下，它显示“你好，世界！”

让我们进一步了解客户端和服务器在发送HTTP请求和响应之前如何建立TCP连接。为了做到这一点，他们都使用所谓的`sockets`套接字。而不是直接使用浏览器，您将通过在命令行上使用telnet来手动模拟浏览器。

在运行Web服务器的同一台计算机上，在命令行上启动一个`telnet`会话，指定主机连接到本地主机，端口连接到8888，然后按Enter键：

    $ telnet localhost 8888
    Trying 127.0.0.1 …
    Connected to localhost.

此时，您已经与本地主机上运行的服务器建立了TCP连接，并准备好发送和接收HTTP消息。在下图中，您可以看到服务器必须执行的标准过程，以便能够接受新的TCP连接。

![接收套接字](images/2017-07-29/LSBAWS_socket.png)

在同一个telnet会话中，类型为`GET/hello HTTP/1.1`，然后按Enter：

    $ telnet localhost 8888
    Trying 127.0.0.1 …
    Connected to localhost.
    GET /hello HTTP/1.1

    HTTP/1.1 200 OK
    Hello, World!

你只是手动模拟你的浏览器！你发送了一个HTTP请求，并得到一个HTTP响应。这是HTTP请求的基本结构：

![HTTP请求解剖](images/2017-07-29/LSBAWS_HTTP_request_anatomy.png)

在HTTP请求由指示该行的HTTP方法（GET，因为我们要求我们的服务器返回我们的东西），path/hello，指示的“页面”，我们希望在服务器和协议版本上。

为了简单起见，我们的Web服务器在这一点上完全忽略了上述请求行。你可以输入任何垃圾，而不是`GET/hello HTTP/1.1`，你仍然会收到一个“Hello，World！”的回复。

输入请求行并点击Enter后，客户端将请求发送到服务器，服务器读取请求行，打印并返回正确的HTTP响应。

以下是服务器发送回客户端的HTTP响应（在这种情况下为telnet）：

![HTTP响应解剖](images/2017-07-29/LSBAWS_HTTP_response_anatomy.png)

我们来解剖一下 该响应包括状态行HTT/1.1 200 OK，然后是所需的空行，然后是HTTP响应主体。

响应状态行`HTTP/1.1 200 OK`由的HTTP版本，在HTTP状态代码和HTTP状态代码的原因短语OK。当浏览器得到响应时，它显示响应的正文，这就是为什么您在浏览器中看到“Hello，World！”的原因。

这就是Web服务器工作的基本模型。总结一下：Web服务器创建一个侦听套接字，并开始接受一个循环中的新连接。客户端启动TCP连接，并且在成功建立之后，客户端向服务器发送HTTP请求，并且服务器以向用户显示的HTTP响应进行响应。要建立TCP连接，客户端和服务器都使用套接字。

现在，您有一个非常基本的工作Web服务器，您可以使用浏览器或其他HTTP客户端进行测试。您已经看到并希望尝试，您也可以通过使用telnet并手动输入HTTP请求来成为人类的HTTP客户端。

这里有一个问题：“如何在新建的Web服务器下运行Django、Flask、Pyramid应用程序，而不必对服务器进行单一更改，以适应所有这些不同的Web框架？

我会在这个系列的第2部分中详细介绍一下。敬请关注。

---

<h1 id="2.0">Part2</h1>

请记住，在第1部分中，我问过一个问题：“如何在新建的Web服务器下运行Django、Flask和Pyramid应用程序，而不必对服务器进行单一更改以适应所有这些不同的Web框架？”找出答案。

过去，您选择的Python Web框架将限制您选择可用的Web服务器，反之亦然。如果框架和服务器被设计为一起工作，那么你还可以。但是，当尝试将服务器和框架组合在一起时，您可能已经面临（或许您是）遇到以下问题：服务器框架冲突 基本上你必须使用一起工作，而不是你可能想要使用的东西。

那么，如何才能确保您可以使用多个Web框架运行Web服务器，而不必对Web服务器或Web框架进行代码更改。而且这个问题的答案就变成了`Python WebServer Gateway Interface`（或简称为WSGI，发音为“wizgy”）


WSGI允许开发人员将Web框架的选择与Web服务器的选择分开。现在，您可以实际混合和匹配Web服务器和Web框架，并选择一个符合您需求的配对。您可以运行Django、Flask和Pyramid，与Gunicorn、Nginx/ uWSGI和Waitress。真正的混搭，感谢WSGI对服务器和框架中的支持：

![混搭](images/2017-07-29/lsbaws_part2_wsgi_interop.png)

所以，WSGI是我在第一部分中问你的问题的答案，并在本文开头重复。您的Web服务器必须实现WSGI接口的服务器部分，并且所有现代Python Web框架都已经实现了WSGI接口的框架端，允许您将其与Web服务器一起使用，而无需修改服务器的代码以适应特定的Web框架。

现在，您知道Web服务器和Web框架的WSGI支持允许您选择适合您的配对，但它也对服务器和框架开发人员有利，因为它们可以专注于其首选的专业领域，而不是相互对峙。其他语言也有类似的接口：例如，Java具有Servlet API，Ruby具有Rack。

这一切都很好，但我敢打赌你在说：“给我看看代码！”好的，看看这个非常简约的WSGI服务器实现：[webserver2.py](part2/webserver2.py)

它绝对大于第1部分中的服务器代码，但它也足够小（只有150行），以便您了解而不会陷入细节。上面的服务器也做了更多的工作 - 它可以运行您所熟悉的Web框架编写的基本Web应用程序，无论是Pyramid，Flask，Django还是其他一些Python WSGI框架。

不相信我 尝试一下，看看自己。将上述代码保存为webserver2.py或直接从GitHub下载。如果您尝试运行它没有任何参数，它会抱怨并退出。

    $ python webserver2.py
    Provide a WSGI application object as module:callable

它真的想要为您的Web应用程序提供服务，这就是开始的乐趣。要运行服务器，唯一需要安装的是Python。但是要运行使用Pyramid，Flask和Django编写的应用程序，您需要首先安装这些框架。我们来安装所有这三个。我的首选方法是使用virtualenv。只需按照以下步骤创建和激活一个虚拟环境，然后安装所有三个Web框架。

    $ [sudo] pip install virtualenv
    $ mkdir ~/envs
    $ virtualenv ~/envs/lsbaws/
    $ cd ~/envs/lsbaws/
    $ ls
    bin  include  lib
    $ source bin/activate
    (lsbaws) $ pip install pyramid
    (lsbaws) $ pip install flask
    (lsbaws) $ pip install django

此时，您需要创建一个Web应用程序。先从pyramid开始吧。将代码保存为pyramidapp.py到您保存webserver2.py的同一目录或直接从GitHub下载文件：[pyramidapp.py](part2/pyramidapp.py)

现在，您可以使用自己的Web服务器为您的Pyramid应用程序提供服务：

    (lsbaws) $ python webserver2.py pyramidapp:app
    WSGIServer: Serving HTTP on port 8888 ...

你只是告诉你的服务器从python模块'pyramidapp'加载'app'可调用您的服务器现在已经准备好接受请求并将其转发到您的Pyramid应用程序。该应用程序现在只处理一条路由：/hello路由。将[http://localhost:8888/hello](http://localhost:8888/hello)地址输入到你的浏览器中，按Enter键，并观察结果：

    Hello world from Pyramid!

您还可以使用`curl`实用程序在命令行中测试服务器：

    $ curl -v http://localhost:8888/hello

检查服务器和curl打印到标准输出。

现在到Flask。让我们按照同样的步骤保存为:[flaskapp.py](part2/flaskapp.py)

并以下列方式运行服务器：

    (lsbaws) $ python webserver2.py flaskapp:app
    WSGIServer: Serving HTTP on port 8888 ...

现在在您的浏览器中输入[http://localhost:8888/hello](http://localhost:8888/hello)，然后按Enter键：

    Hello world from Flask!

再次尝试'curl'，看看自己，服务器返回由Flask应用程序生成的消息

服务器还能处理Django应用程序吗？试试看！然而，这有点更多的涉及，我建议克隆整个repo并使用djangoapp.py，它是GitHub存储库的一部分。这是源代码，它将Django'helloworld '项目（使用Django的django-admin.py startproject命令预先创建）添加到当前的Python路径中，然后导入项目的WSGI应用程序。

将代码保存为:[djangoapp.py](part2/djangoapp.py)

并使用Web服务器运行Django应用程序：

    (lsbaws) $ python webserver2.py djangoapp:app
    WSGIServer: Serving HTTP on port 8888 ...

输入以下地址，然后按Enter：

    Hello world from Flask!

而且你以前已经做过几次，你可以在命令行上测试它，并确认这是Django应用程序处理你的请求

好的，您已经体验到了WSGI的强大功能：它允许您混合和匹配Web服务器和Web框架。WSGI提供了Python Web服务器和Python Web框架之间的最小接口。它非常简单，并且在服务器和框架端都很容易实现。以下代码片段显示了该接口的服务器端和框架端：

    def run_application(application):
        """Server code."""
        # This is where an application/framework stores
        # an HTTP status and HTTP response headers for the server
        # to transmit to the client
        headers_set = []
        # Environment dictionary with WSGI/CGI variables
        environ = {}

        def start_response(status, response_headers, exc_info=None):
            headers_set[:] = [status, response_headers]

        # Server invokes the ‘application' callable and gets back the
        # response body
        result = application(environ, start_response)
        # Server builds an HTTP response and transmits it to the client
        …

    def app(environ, start_response):
        """A barebones WSGI app."""
        start_response('200 OK', [('Content-Type', 'text/plain')])
        return ['Hello world!']

    run_application(app)

下面是它的工作原理：

1. 该框架提供了一个可调用`application`（WSGI规范未规定应如何实现）
2. 服务器对从HTTP客户端接收到的每个请求调用`application`。它传递一个包含`WSGI/CGI`变量的字典`environ`，并将`start_response`作为参数传递给可调用`application` 。
3. 框架/应用程序生成HTTP status和HTTP response，并将它们传递给服务器可以存储的`start_response`。框架/应用程序还返回一个响应体。
4. 服务器将status，response headers和response body组合到HTTP响应中并将其传输到客户端（此步骤不是规范的一部分，但它是流程中的下一个逻辑步骤，为了清楚起见，我添加了它）

这里是界面的视觉表示：

![WSGI接口](images/2017-07-29/lsbaws_part2_wsgi_interface.png)

到目前为止，您已经看到了Pyramid，Flask和Django Web应用程序，您已经看到实现WSGI规范的服务器端的服务器代码。您甚至看到了不使用任何框架的准系统WSGI应用程序代码片段。

事实是，当您使用其中一个框架编写Web应用程序时，您可以在较高级别工作并且不直接使用WSGI，但是我知道您对WSGI界面的框架方面感到好奇，因为您正在读这篇文章。所以，让我们创建一个简约的WSGI Web application/ Web framework，而不必使用Pyramid，Flask或Django，并与您的服务器一起运行：

    def app(environ, start_response):
        """A barebones WSGI application.

        This is a starting point for your own Web framework :)
        """
        status = '200 OK'
        response_headers = [('Content-Type', 'text/plain')]
        start_response(status, response_headers)
        return ['Hello world from a simple WSGI application!\n']

再次，将上述代码保存在wsgiapp.py文件中，或直接从GitHub下载，并在Web服务器下运行应用程序：

    (lsbaws) $ python webserver2.py wsgiapp:app
    WSGIServer: Serving HTTP on port 8888 ...

键入以下地址，然后按Enter键。这是你应该看到的结果：

    Hello world from a simple WSGI application!

您刚刚写了您自己的简约WSGI Web框架，同时了解如何创建Web服务器！抱得美人归。

现在，让我们回到服务器发送给客户端的内容。以下是使用HTTP客户端调用Pyramid应用程序时，服务器生成的HTTP响应：

![HTTP响应第1部分](images/2017-07-29/lsbaws_part2_http_response.png)

响应有一些熟悉的部分，你在第1部分看到，但它也有一些新的东西。它具有例如以前没有看到的四个HTTP头：内容类型，内容长度，日期和服务器。这些是Web服务器响应一般应该具有的标题。但是，这些都不是严格要求的。标头的目的是传输关于HTTP  请求/响应的附加信息。

现在您了解更多有关WSGI接口的信息，这里是HTTP响应的一些相关信息，有关哪些部件生成的信息呢？

![HTTP响应第2部分](images/2017-07-29/lsbaws_part2_http_response_explanation.png)

我还没有说过“environ”字典，但基本上它是一个Python字典，必须包含WSGI规范规定的某些WSGI和CGI变量。解析请求后，服务器从HTTP请求中获取字典的值。这是字典的内容如下所示：

![环境Python字典](images/2017-07-29/lsbaws_part2_environ.png)

Web框架使用该字典中的信息根据指定的路由，请求方法等决定使用哪个视图，从哪里读取请求主体以及在哪里写入错误（如果有的话）。

到目前为止，您已经创建了自己的WSGI Web服务器，并且使用不同的Web框架编写了Web应用程序。而且，您还创建了您的准系统Web应用程序/ Web框架。这是一场旅程的跋涉。让我们回顾一下WSGI Web服务器为WSGI  应用程序提供的请求所做的工作：

+ 首先，服务器启动并加载由Web框架/应用程序提供的“应用程序”调用
+ 然后，服务器读取一个请求
+ 然后，服务器解析它
+ 然后，它使用请求数据构建一个“环境”字典
+ 然后，它使用'environ'字典和'start_response'调用作为参数调用'application'，并返回一个响应体。
+ 然后，服务器使用由'application'对象调用返回的数据和由'start_response'callable设置的状态和响应标头来构造一个HTTP响应 。
+ 最后，服务器将HTTP响应发送回客户端

![服务器摘要](images/2017-07-29/lsbaws_part2_server_summary.png)

这就是所有的一切。您现在拥有一个工作的WSGI服务器，可以提供使用符合WSGI标准的Web框架（如Django，Flask，Pyramid）或您自己的WSGI框架编写的基本Web应用程序。最好的部分是服务器可以与多个Web框架一起使用，而不会对服务器代码库进行任何更改。一点也不差。

在你走之前，这里是另一个问题，您可以考虑一下，“您如何使您的服务器一次处理多个请求？”

请继续关注，我会在第3部分向您展示一种方法。干杯！

---

# Part3


在第2部分中，您创建了一个可以处理基本HTTP GET请求的简约WSGI服务器。我问你一个问题，“你如何使您的服务器一次处理多个请求？”在本文中，您将找到答案。所以，扣起来，转入高档。你要快一点 准备好您的Linux，Mac OS X（或任何* nix系统）和Python。本文中的所有源代码均可在GitHub上找到。

首先让我们记住一个非常基本的Web服务器，以及服务器需要做什么来为客户端请求提供服务。您在第1部分和第2 部分中创建的服务器是一次处理一个客户端请求的迭代服务器。在完成处理当前客户端请求之后，它不能接受新的连接。有些客户可能不满意，因为它们必须排队等待，而对于繁忙的服务器，该行可能太长。


以下是迭代服务器webserver3a.py的代码：[webserver3a.py](part3/webserver3a.py)

为了观察您的服务器一次只处理一个客户端请求，请稍等一点修改服务器，并在向客户端发送响应后再延迟60秒。更改只是一行告诉服务器进程睡眠60秒。

这里是睡眠服务器webserver3b.py的代码：[webserver3b.py](part3/webserver3b.py)

启动服务器：

    $ python webserver3b.py
现在打开一个新的终端窗口并运行curl命令。您应该立即看到屏幕上打印的“Hello，World！”字符串

    $ curl http://localhost:8888/hello
    Hello, World!

并且无延迟打开第二个终端窗口并运行相同的curl命令：

    $ curl http://localhost:8888/hello

如果您在60秒内完成了此操作，那么第二个curl不应立即产生任何输出，而应该挂在那里。服务器也不应在其标准输出上打印新的请求体。这是Mac上的样子（右下角的窗口以黄色突出显示第二个curl命令挂起，等待连接被服务器接受）：

[](images/2017-07-29/lsbaws_part3_it3.png)

你已经等待之后足够长（超过60秒），你应该看到的第一个curl终止和第二curl打印“你好，世界！”在屏幕上，然后挂60秒，然后终止：

[](images/2017-07-29/lsbaws_part3_it4.png)

它的工作方式是服务器完成第一个curl客户端请求的服务，然后仅在休眠60秒后才开始处理第二个请求。这一切都是顺序地，或迭代地，一次，或在我们的情况下，一次客户端请求。

让我们谈一谈客户端和服务器之间的沟通。为了使两个程序通过网络进行通信，必须使用套接字。而您在第1 部分和第2 部分中看到了插座。但是什么是`socket`接字？

[](images/2017-07-29/lsbaws_part3_it_socket.png)

一个套接字是通信端点的抽象，它可以让你的程序使用文件描述符另一个程序进行通信。在本文中，我将特别谈到Linux/Mac OS上的TCP/IP套接字。一个重要的理解是TCP套接字对。

>  套接字对一个TCP连接是4元组标识的两个端点TCP连接：本地IP地址，本地端口，国外IP地址和外部端口。套接字对唯一标识网络上的每个TCP连接。识别每个端点的两个值，IP地址和端口号通常称为套接字。

[](images/2017-07-29/lsbaws_part3_it_socketpair.png)

所以，元组{10.10.10.2:49152,12.12.12.3:8888}是一个套接字对，可以唯一标识客户端上TCP连接的两个端点，元组{12.12.12.3:8888,10.10.10.2:49152}是一个套接字对，可以唯一标识服务器上TCP连接的两个端点。标识TCP连接的服务器端点（IP地址12.12.12.3和端口8888）的两个值在这种情况下被称为套接字（同样适用于客户机端点）。

服务器通常创建套接字并开始接受客户端连接的标准顺序如下：

[](images/2017-07-29/lsbaws_part3_it_server_socket_sequence.png)

1. 服务器创建一个TCP / IP套接字。这是用Python中的以下语句完成的：

    listen_socket = socket.socket（socket.AF_INET，socket.SOCK_STREAM）

2. 服务器可能会设置一些套接字选项（这是可选的，但是您可以看到，如果您决定杀死并重新启动服务器，上述服务器代码就能够重复使用相同的地址远）。

    listen_socket.setsockopt（socket.SOL_SOCKET，socket.SO_REUSEADDR，1）

3. 然后，服务器绑定地址。该绑定函数分配一个本地协议地址到插座。使用TCP，调用绑定可以指定端口号，IP地址，两者或两者。1

    listen_socket.bind（SERVER_ADDRESS）

4. 然后，服务器使套接字成为一个监听套接字

    listen_socket.listen（REQUEST_QUEUE_SIZE）

该听方法仅由所谓的服务器。它告诉内核它应该接受此套接字的传入连接请求。

完成后，服务器一次开始接受客户端连接一个连接。当有可用的连接时，接受呼叫返回连接的客户端套接字。然后，服务器从连接的客户端套接字中读取请求数据，将数据打印在其标准输出上，并将消息发送回客户端。然后，服务器关闭客户端连接，它再次准备好接受新的客户端连接。

以下是客户端通过TCP/IP与服务器通信所需要做的事情：

[](images/2017-07-29/lsbaws_part3_it_client_socket_sequence.png)

以下是客户端连接到服务器的示例代码，发送请求并打印响应：

    import socket

    # create a socket and connect to a server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 8888))

    # send and receive some data
    sock.sendall(b'test')
    data = sock.recv(1024)
    print(data.decode())

创建套接字后，客户端需要连接到服务器。这是通过连接调用完成的：

    sock.connect(('localhost', 8888))

客户端只需要提供要连接的服务器的远程IP地址或主机名以及远程端口号。

您可能已经注意到客户端不调用绑定和接受。客户端不需要调用绑定，因为客户端不关心本地IP地址和本地端口号。当客户端呼叫连接时，内核中的TCP/IP堆栈自动分配本地IP地址和本地端口。本地港口称为短暂港口，即短暂港口。



标识客户端连接的知名服务的服务器上的端口称为公知端口（例如，HTTP为HTTP，SSH为22 ）。启动您的Python shell，并与客户端连接到在localhost上运行的服务器，并查看内核分配给您创建的套接字的临时端口（在尝试以下示例之前启动服务器webserver3a.py或webserver3b.py）：

```
    >>> import socket
    >>> sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    >>> sock.connect(('localhost', 8888))
    >>> host, port = sock.getsockname()[:2]
    >>> host, port
    ('127.0.0.1', 60589)
```

在上述情况下，内核将临时端口60589分配给插座。

在我回答第二部分的问题之前，还有一些其他重要的概念，我需要快速的介绍。你很快就会看到为什么这很重要。这两个概念是一个process进程和一个file descriptor文件描述符。

什么是进程？一个进程就是一个执行程序的实例。例如，当服务器代码被执行时，它被加载到内存中，该执行程序的实例被称为进程。内核记录一系列有关进程的信息 - 其进程ID将是一个示例 - 来跟踪它。当您运行迭代服务器webserver3a.py或webserver3b.py时，您只运行一个进程。



在终端窗口中启动服务器webserver3b.py：

    $ python webserver3b.py

在不同的终端窗口中，使用ps命令获取有关该进程的信息：

    $ ps | grep webserver3b | grep -v grep
    7182 ttys003    0:00.04 python webserver3b.py

该PS命令显示你，你的确只运行一个Python进程webserver3b。当进程创建时，内核会为其分配进程ID（PID）。在UNIX，每个用户进程也有父母，反过来，有其自己的进程ID叫父进程ID，或PPID的简称。我假设你运行BASH由默认的shell，当你启动服务器，新工艺得到了创建PID与其父PID设定为PID的的BASH shell。



尝试一下，看看自己一切如何工作。再次打开你的Python shell，这将创造一个新的进程，然后拿到PID Python的shell进程和父PID（的PID您的BASH使用shell）os.getpid（）和os.getppid（）系统调用。然后，在另一个终端窗口中运行ps命令和grep的PPID（父进程ID，在我的情况下是3148）。在下面的截图中，您可以看到我的Mac OS X上的子代Python shell进程和父BASH shell进程之间的父子关系的示例：

![](images/2017-07-29/lsbaws_part3_it_pid_ppid_screenshot.png)

另一个重要的概念就是file descriptor文件描述符。那么什么是文件描述符？一个文件描述符是一个非负整数内核时，它会打开一个现有文件，创建一个新的文件，或者当它创建了一个新的socket返回的过程。你可能听说过UNIX中的一切都是文件。内核通过文件描述符引用进程的打开文件。当您需要读取或写入文件时，您可以使用文件描述符来标识它。Python为您提供高级对象来处理文件（和套接字），并且您不必直接使用文件描述符来标识文件，但是在引擎盖下，这就是UNIX中标识文件和套接字的方式：以其整型文件描述。

![](images/2017-07-29/lsbaws_part3_it_process_descriptors.png)

默认情况下，UNIX shell将文件描述符0分配给进程的标准输入，文件描述符1分配给标准输出的进程和文件描述符2到标准错误。

![](images/2017-07-29/lsbaws_part3_it_default_descriptors.png)

如前所述，尽管Python为您提供了一个高级文件或类似文件的对象，但您可以随时使用对象上的fileno（）方法来获取与该文件相关联的文件描述符。回到你的Python shell，看看你能做到这一点：
```
    >>> import sys
    >>> sys.stdin
    <open file '<stdin>', mode 'r' at 0x102beb0c0>
    >>> sys.stdin.fileno()
    0
    >>> sys.stdout.fileno()
    1
    >>> sys.stderr.fileno()
    2
```
而在Python中使用文件和套接字时，通常会使用high-level file/socket object(高级文件/套接字对象)，但是可能需要直接使用文件描述符。下面是一个使用一个写入系统调用将文件描述符整数作为参数将字符串写入标准输出的示例：
```
    >>> import sys
    >>> import os
    >>> res = os.write(sys.stdout.fileno(), 'hello\n')
    hello
```
这是一个有趣的部分 - 这不应该让你感到惊讶，因为你已经知道一切都是Unix中的一个文件 - 你的套接字也有一个文件描述符与它相关联。再次，当您在Python中创建一个套接字时，您将返回一个对象而不是一个非负整数，但是您可以随时使用前面提到的fileno（）方法直接访问套接字的整数文件描述符。
```
    >>> import socket
    >>> sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    >>> sock.fileno()
    3
```
还有一件事我想提到：您是否注意到，在第二个迭代服务器webserver3b.py的例子中，当服务器进程休眠60秒时，您仍然可以使用第二个curl命令连接到服务器？当然curl没有立即输出任何东西，只是挂在那里，但是服务器当时没有接受连接，客户端没有立即被拒绝，而是能够连接到服务器？答案是socket对象的listen方法及其BACKLOG参数，我在代码中调用了REQUEST_QUEUE_SIZE。BACKLOG参数确定内核中传入连接请求的队列大小。当服务器webserver3b.py正在休眠时，您运行的第二个curl命令能够连接到服务器，因为内核在服务器套接字的传入连接请求队列中有足够的可用空间。

在增加BACKLOG参数的同时，并不会让您的服务器变成一次可以处理多个客户端请求的服务器，因此对于繁忙的服务器来说，拥有相当大的积压参数非常重要，因此接受呼叫不必等待新的连接将被建立，但可以立即从新队列中取出新连接，并立即开始处理客户端请求。

喔，呼！你已经覆盖了很多地面。到目前为止，我们可以快速回顾一下你所学到的内容（如果这些都是基础知识，那么刷新）。

![](images/2017-07-29/lsbaws_part3_checkpoint.png)

- 迭代服务器
- 服务器套接字创建顺序（socket，bind，listen，accept）
- 客户端连接创建顺序（套接字，连接）
- 套接字对
- 插座
- 短暂港口和知名港口
- 处理
- 进程ID（PID），父进程标识（PPID）和父子关系。
- 文件描述符
- listen socket方法的BACKLOG参数的含义

现在我已经准备好回答第2部分的问题：“您如何使服务器一次处理多个请求？”或者换句话说，“如何编写并发服务器？”



在Unix下编写并发服务器的最简单方法是使用fork（）系统调用。



这是新的闪存并发服务器webserver3c.py的代码，可以同时处理多个客户端请求（如我们的迭代服务器示例webserver3b.py，每个子进程休眠60秒）：[webserver3c.py](part3/webserver3c.py)

在潜水和讨论fork如何工作之前，尝试一下，并且看到自己，服务器可以确实同时处理多个客户端请求，而不像它的迭代对应的webserver3a.py和webserver3b.py。在命令行上启动服务器：

    $ python webserver3c.py

并尝试使用与迭代服务器相同的两个curl命令，并自己看看，即使服务器子进程在服务客户端请求后休眠了60秒，因为它们不会影响其他客户端由不同而完全独立的过程服务。你应该看到你的curl命令立即输出“Hello，World！”，然后挂起60秒。您可以继续运行尽可能多的curl命令（也就是你想要的几乎一样多），所有这些都将立即输出服务器的响应“Hello，World”，而不会有明显的延迟。尝试一下。

了解fork（）的最重要的一点是你调用fork一次，但是它返回两次：一次在父进程中，一次在子进程中。当您分叉一个新进程时，返回到子进程的进程ID为0.当fork返回父进程时，它返回子进程的PID。

![](images/2017-07-29/lsbaws_part3_conc2_how_fork_works.png)

我还记得当我第一次阅读并尝试的时候，我被fork着迷了。对我来说看起来像是魔术。在这里，我正在阅读一个顺序代码，然后是“繁荣！”：代码克隆了自己，现在有两个同时运行的同时运行的实例。我以为这不是魔术，而是认真的。

当父母为新孩子分配时，子进程将获取父文件描述符的副本：

![](images/2017-07-29/lsbaws_part3_conc2_shared_descriptors.png)

您可能已经注意到，上述代码中的父进程关闭了客户端连接：

    else:  # parent
        client_connection.close()  # close parent copy and loop over

那么子进程如何才能从客户端套接字读取数据，如果它的父级关闭了相同的套接字？答案在上图。内核使用描述符引用计数来决定是否关闭套接字。只有当它的描述符引用计数为0时，才会关闭该套接字。当您的服务器创建一个子进程时，该子进程将获取父文件描述符的副本，并且内核会为这些描述符增加引用计数。在一个父和一个孩子的情况下，对于客户端套接字，描述符引用计数将为2，并且当上述代码中的父进程关闭客户端连接套接字时，它仅将其引用计数递减为1，不足够小使内核关闭套接字。

    listen_socket.close()  # close child copy

我将讨论如果在文章后面没有关闭重复描述符会发生什么。

从并发服务器的源代码可以看出，服务器父进程的唯一作用是接受新的客户端连接，fork一个新的子进程来处理该客户端请求，并循环接受另一个客户端连接，没什么了 服务器父进程不处理客户端请求 - 其子进程。

一点点 当我们说两个事件是并发的时候是什么意思？

![](images/2017-07-29/lsbaws_part3_conc2_concurrent_events.png)

当我们说两个事件并发时，我们通常意味着它们同时发生。作为一个速记，定义很好，但你应该记住严格的定义：

如果您不能通过查看将首先发生的程序来判断两个事件是并发的。2
再次，现在是回顾你迄今为止所涵盖的主要思想和概念。

![](images/2017-07-29/lsbaws_part3_checkpoint.png)

- 在Unix中编写并发服务器的最简单的方法是使用fork（）系统调用
- 当进程分派新进程时，它将成为新分支子进程的父进程。
- 调用fork后，父和子共享相同的文件描述符。
- 内核使用描述符引用计数来决定是否关闭文件/套接字
- 服务器父进程的作用：它现在所做的是接受来自客户端的新连接，fork一个子进程来处理客户端请求，并循环接受一个新的客户端连接。

让我们看看如果在父进程和子进程中没有关闭重复的套接字描述符，将会发生什么。以下是并发服务器的修改版本，其中服务器不会关闭重复的描述符:[webserver3d.py](part3/webserver3d.py)

启动服务器：

    $ python webserver3d.py

使用curl连接到服务器：

    $ curl http://localhost:8888/hello
    Hello, World!

好的，curl打印了来自并发服务器的响应，但没有终止并保持挂起。这里发生了什么？服务器不再睡眠60秒：其子进程主动处理客户端请求，关闭客户端连接并退出，但客户端curl仍然不会终止。



那么为什么curl不会终止？原因是重复的文件描述符。当子进程关闭客户端连接时，内核递减该客户端套接字的引用计数，计数为1。服务器子进程退出，但客户端套接字未被内核关闭，因为该套接字描述符的引用计数为不为0，并且，作为结果，终止数据包（称为FIN在TCP / IP的说法）未发送到客户端，在客户端停留就行，可以这么说。还有另一个问题。如果您的长时间运行的服务器不会关闭重复的文件描述符，则最终将耗尽可用的文件描述符：

![](images/2017-07-29/lsbaws_part3_conc3_out_of_descriptors.png)

使用Control-C停止服务器webserver3d.py，并使用shell内置命令ulimit查看您的shell设置的服务器进程可用的默认资源

    $ ulimit -a
    core file size          (blocks, -c) 0
    data seg size           (kbytes, -d) unlimited
    scheduling priority             (-e) 0
    file size               (blocks, -f) unlimited
    pending signals                 (-i) 3842
    max locked memory       (kbytes, -l) 64
    max memory size         (kbytes, -m) unlimited
    open files                      (-n) 1024
    pipe size            (512 bytes, -p) 8
    POSIX message queues     (bytes, -q) 819200
    real-time priority              (-r) 0
    stack size              (kbytes, -s) 8192
    cpu time               (seconds, -t) unlimited
    max user processes              (-u) 3842
    virtual memory          (kbytes, -v) unlimited
    file locks                      (-x) unlimited

如上所示，Ubuntu的服务器进程可用的最大打开文件描述符（打开文件）数为1024。

现在让我们看看如果服务器不能关闭重复的描述符，可以使用可用的文件描述符。在现有或新的终端窗口中，将服务器的打开文件描述符的最大数量设置为256：

    $ ulimit -n 256

在刚刚运行$ ulimit -n 256  命令的同一终端中启动服务器webserver3d.py：

    $ python webserver3d.py

并使用以下客户端client3.py来测试服务器: [client3.py](part3/client3.py)



在新的终端窗口中，启动client3.py并告诉它创建与服务器的300个并发连接：

    $ python client3.py --max-clients=300

很快你的服务器会爆炸。这是我的框上的例外的屏幕截图：

![](images/2017-07-29/lsbaws_part3_conc3_resource_unavailable.png)

这个教训很清楚 - 你的服务器应该关闭重复的描述符。但是即使你关闭重复的描述符，你也不会离开树林，因为你的服务器还有一个问题，那个问题就是僵尸！

![](images/2017-07-29/lsbaws_part3_conc3_zombies.png)

是的，您的服务器代码实际上是创建僵尸。我们来看看怎么样 再次启动您的服务器：

    $ python webserver3d.py

在另一个终端窗口中运行以下curl命令：

    $ curl http://localhost:8888/hello

现在运行ps命令来显示正在运行的Python进程。这个我在Ubuntu框上ps输出的例子：

    $ ps auxw | grep -i python | grep -v grep
    vagrant   9099  0.0  1.2  31804  6256 pts/0    S+   16:33   0:00 python webserver3d.py
    vagrant   9102  0.0  0.0      0     0 pts/0    Z+   16:33   0:00 [python] <defunct>

你看到上面的第二行，它表示PID 9102 的进程状态是Z +，进程的名称是<defunct>？那是我们的僵尸。僵尸的问题是你不能杀死他们。

![](images/2017-07-29/lsbaws_part3_conc3_kill_zombie.png)

即使你尝试用$ kill -9杀死僵尸他们会幸存下来。尝试一下，看看自己。

什么是僵尸，为什么我们的服务器创建它们？一个僵尸是已经终止的过程，但其母公司并没有等待它并没有收到它的终止状态呢。当子进程在其父进程之前退出时，内核会将子进程转换为僵尸，并存储有关进程的一些信息以供其父进程稍后检索。存储的信息通常是进程ID，进程终止状态和进程的资源使用情况。好的，所以僵尸有一个目的，但是如果你的服务器没有照顾这些僵尸你的系统会被堵塞。我们来看看怎么回事。首先停止运行的服务器，在新的终端窗口中，

    $ ulimit -u 400
    $ ulimit -n 500

在刚刚运行$ ulimit -u 400命令的同一终端中启动服务器webserver3d.py：

    $ python webserver3d.py

在新的终端窗口中，启动client3.py并告诉它创建与服务器的500个并发连接：

    $ python client3.py --max-clients = 500

而且，再一次，您的服务器很快就会因为OSError而爆炸：资源暂时不可用的异常，当它尝试创建一个新的子进程，但是它不能因为它已经达到允许的最大子进程数限制创建。这是我的框上的例外的屏幕截图：

![](images/2017-07-29/lsbaws_part3_conc3_resource_unavailable.png)

如您所见，僵尸会为您的长时间运行的服务器创建问题，如果它不负责。我将尽快讨论服务器应该如何处理僵尸问题。

让我们回顾一下你到目前为止的要点：

![](images/2017-07-29/lsbaws_part3_checkpoint.png)

- 如果不关闭重复的描述符，则客户端将不会终止，因为客户端连接不会被关闭。
- 如果不关闭重复描述符，则长时间运行的服务器最终将耗尽可用的文件描述符（最大打开文件）。
- 当您分支子进程并退出并且父进程不等待它，并且不会收到其终止状态时，它将成为一个僵尸。
- 僵尸需要吃东西，在我们的情况下，它是记忆。如果您的服务器不能处理僵尸，最终将耗尽可用进程（最多用户进程）。
- 不能杀死一个僵尸，你需要等待它。

那么你需要做些什么来照顾僵尸呢？您需要修改服务器代码以等待僵尸才能获得终止状态。您可以通过修改服务器来调用等待系统调用。不幸的是，这远不是理想的，因为如果您打电话等待，并且没有终止的子进程，则等待的调用将阻止您的服务器，从而有效地防止您的服务器处理新的客户端连接请求。还有其他选择吗？是的，有，其中之一是信号处理程序与等待系统调用的组合。



下面是它的工作原理。当子进程退出时，内核发送一个SIGCHLD信号。父进程可以设置异步通知该SIGCHLD事件的信号处理程序，然后可以等待小孩收集其终止状态，从而防止僵尸进程遗留。

![](images/2017-07-29/lsbaws_part_conc4_sigchld_async.png)

顺便说一句，异步事件意味着父进程不提前知道事件将会发生。

修改您的服务器代码以设置SIGCHLD事件处理程序，并等待事件处理程序中的终止子进程。该代码在webserver3e.py文件中可用：[webserver3e.py](part3/webserver3e.py)



启动服务器：

    $ python webserver3e.py

使用您的老朋友curl向修改的并发服务器发送请求：

    $ curl http：// localhost：8888 / hello

看看服务器：

![](images/2017-07-29/lsbaws_part3_conc4_eintr.png)

刚刚发生了什么？接受呼叫失败，并显示错误EINTR。



当子进程退出时，父进程在接受调用中被阻塞，从而导致SIGCHLD事件，后者又激活了信号处理程序，当信号处理程序完成接受系统调用时中断：



不用担心，这是一个非常简单的问题要解决。所有您需要做的是重新启动接受系统调用。以下是处理该问题的服务器webserver3f.py的修改版本：[webserver3f.py](part3/webserver3f.py)


启动更新的服务器webserver3f.py：

    $ python webserver3f.py

使用curl向修改的并发服务器发送请求：

    $ curl http：// localhost：8888 / hello

看到？没有EINTR例外。现在，验证没有更多的僵尸，并且您的等待呼叫的SIGCHLD事件处理程序照顾终止的孩子。要做到这一点，只需运行ps命令，看看自己没有更多的Python进程具有Z +状态（不再有<已停止>进程）。大！没有僵尸奔跑，感觉安全。

![](images/2017-07-29/lsbaws_part3_checkpoint.png)

- 如果你分叉一个孩子，不要等待它，它就变成一个僵尸。
- 使用SIGCHLD事件处理程序异步等待终止的子进程终止状态
- 当使用事件处理程序时，您需要记住，系统调用可能会中断，您需要为此方案做好准备

好的，到目前为止这么好。没问题，对吧？好吧，差不多 再次尝试您的webserver3f.py，而不是使用curl使一个请求使用client3.py创建128个并发连接：

    $ python client3.py --max-clients 128

现在再次运行ps命令

    $ ps auxw | grep -i python | grep -v grep

看到，哦，男孩，僵尸又回来了！

![](images/2017-07-29/lsbaws_part3_conc5_zombies_again.png)

这次出了什么问题？当您运行128个并发客户端并建立了128个连接时，服务器上的子进程处理请求并几乎同时退出，导致大量SIGCHLD信号被发送到父进程。问题是信号不排队，您的服务器进程丢失了几个信号，这使得几个僵尸无人值守运行：

![](images/2017-07-29/lsbaws_part3_conc5_signals_not_queued.png)

问题的解决方案是设置一个SIGCHLD事件处理程序，而不是等待在循环中使用带有WNOHANG选项的waitpid系统调用，以确保所有已终止的子进程得到处理。这是修改后的服务器代码，webserver3g.py：[webserver3g.py](part3/webserver3g.py)


启动服务器：

    $ python webserver3g.py

使用测试客户端client3.py：

    $ python client3.py --max-clients 128

现在验证没有更多的僵尸。好极了！没有僵尸的生活是好的:)

![](images/2017-07-29/lsbaws_part3_conc5_no_zombies.png)

恭喜！这是一个漫长的旅程，但我希望你喜欢它。现在，您有自己的简单的并发服务器，代码可以作为进一步开展生产级Web服务器的基础。

我将把它作为练习，让您从第2部分更新WSGI服务器并使其并发。您可以在这里找到修改版本。但是，只有在您实现了自己的版本后才能看到我的代码。你有所有必要的信息来做到这一点。所以去，只是做它:)

下一步是什么？正如乔希比林斯所说，

> “Be like a postage stamp — stick to one thing until you get there.”

开始掌握基础知识。问你已经知道了什么 并且总是深入挖掘。

> “If you learn only methods, you’ll be tied to your methods. But if you learn principles, you can devise your own methods.” —Ralph Waldo Emerson
