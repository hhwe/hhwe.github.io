## 一次HTTP请求经历了什么

+ 首先在浏览器中敲下URL, 我们需要通过URL找到对应的IP地址
    1. 浏览器会从缓存中读取DNS, 
    2. 从OS的hosts读取DNS
    3. 通过DNS服务器读取, 
    4. 没找到在从上一级DNS读取
+ 找到IP后通过三次握手建立TCP连接
+ 浏览器发送HTTP请求给服务器
+ 服务器收到请求后发送相应的HTTP响应
+ 浏览器受到响应和相应的资源文件后渲染页面
+ 最后浏览器会断开TCP连接

## HTTP协议

HTTP是一种让Web服务器与浏览器(客户端)通过Internet发送与接收数据的协议,它建立在TCP协议之上，一般采用TCP的80端口。它是一个请求、响应协议，客户端发出一个请求，服务器响应这个请求。在HTTP中，客户端总是通过建立一个连接与发送一个HTTP请求来发起一个事务。服务器不能主动去与客户端联系，也不能给客户端发出一个回调连接。客户端与服务器端都可以提前中断一个连接。

HTTP协议是无状态的，同一个客户端的这次请求和上次请求是没有对应关系，对HTTP服务器来说，它并不知道这两个请求是否来自同一个客户端。为了解决这个问题， Web程序引入了Cookie机制来维护连接的可持续状态。

### Request
``` http
GET / HTTP/1.1    //请求行: 请求方法 请求URI HTTP协议/协议版本
Host: www.baidu.com    // 服务器主机
Connection: keep-alive    // 保持TCP连接，单次连接多次请求
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit
Accept: text/html,application/xhtml+xml   // 客户端能接收的MIME
Accept-Encoding: gzip, deflate, br    // 是否支持流压缩
Accept-Language: zh-CN,zh;q=0.9
Cookie: BDSVRTM=0;
```
请求方法：
+ GET：获取服务器资源
+ POST： 向服务器提交资源
+ PUT： 修改资源，全部覆盖原先资源
+ PATCH：修改资源，可以单独修改要修改的字段
+ DELETE： 删除资源
### Response
``` http
HTTP/1.1 200 OK    // 版本号，状态码，状态消息
Cache-Control: private
Connection: Keep-Alive    //HTTP1.1引入
Content-Encoding: gzip
Content-Type: text/html
Date: Sun, 15 Jul 2018 05:40:19 GMT
Expires: Sun, 15 Jul 2018 05:40:10 GMT
Server: BWS/1.1    //服务器软件名版本
Set-Cookie: BDSVRTM=0; path=/
Strict-Transport-Security: max-age=172800
Vary: Accept-Encoding
X-Ua-Compatible: IE=Edge,chrome=1
Transfer-Encoding: chunked    //分段发送HTTP包
```
响应状态码：
+ 1XX 提示信息 - 表示请求已被成功接收，继续处理
+ 2XX 成功 - 表示请求已被成功接收，理解，接受
+ 3XX 重定向 - 要完成请求必须进行更进一步的处理
+ 4XX 客户端错误 - 请求有语法错误或请求无法实现
+ 5XX 服务器端错误 - 服务器未能实现合法的请求

## http1.0 vs http1.1 
1. http1.1支持单个tcp链接传输多个http请求通过请求头`Connection: keep-alive`
2. http1.1添加了几个请求方法`HEADER`,`PATCH`节约带宽
3. http1.1支持断点续传,客户端发请求时对应的是`Range` ，服务器端响应时对应的是`Content-Range`

## http1.1 vs http2.0
*   **单个TCP链接.** 服务器加载网站会尽可能的保持单个TCP链接, 减少了很多琐碎的tcp链接,直到页面关闭
*   **多路复用.** 单次链接中可以同时处理多个请求, 而在http1.1中每次传输会等待上次传输结束
*   **服务推送.** 额外的资源会推送给客户端以后使用, 单个请求中返回需要的所有资源文件
*   **有优先级.** 请求有分配等级服务器可以使得等级高的请求响应更快
*   **二进制.** 使HTTP / 2更易于服务器解析, 更紧凑, 更不容易出错. 没有浪费额外的时间将信息从文本转换为二进制文件, 这是计算机的母语
*   **压缩请求头.** HTTP/2使用HPACK压缩, 减少了重复请求.在HTTP/1.1发送很多相同的请求头.

