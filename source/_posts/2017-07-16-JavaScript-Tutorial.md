---
title: JavaScript-浏览器
date: 2017-07-16 12:01:33
categories: JS
tags: 
    - JS
    - tutorial
---


*   [浏览器](#6.0)
    *   [浏览器对象](#6.1)
    *   [操作DOM](#6.2)
    *   [操作表单](#6.3)
    *   [操作文件](#6.4)
    *   [AJAX](#6.5)
    *   [Promise](#6.6)
    *   [Canvas](#6.7)

---

<h1 id="6.1">浏览器对象</h1>

### window

`window`对象不但充当全局作用域，而且表示浏览器窗口.
`innerWidth`和`innerHeight`属性，可以获取浏览器窗口的内部宽度和高
`outerWidth`和`outerHeight`属性，可以获取浏览器窗口的整个宽度和高

### navigator

`navigator`对象表示浏览器的信息，最常用的属性包括：

- navigator.appName：浏览器名称；
- navigator.appVersion：浏览器版本；
- navigator.language：浏览器设置的语言；
- navigator.platform：操作系统类型；
- navigator.userAgent：浏览器设定的User-Agent字符串。

*注*:navigator的信息可以很容易地被用户修改

### screen

`screen`对象表示屏幕的信息，常用的属性有：

- screen.width：屏幕宽度，以像素为单位；
- screen.height：屏幕高度，以像素为单位；
- screen.colorDepth：返回颜色位数，如8、16、24。

### location

`location`对象表示当前页面的URL信息。

    location.href：http://www.example.com:8080/path/index.html?a=1&b=2#TOP
    location.protocol; // 'http'
    location.host; // 'www.example.com'
    location.port; // '8080'
    location.pathname; // '/path/index.html'
    location.search; // '?a=1&b=2'
    location.hash; // 'TOP'

要加载一个新页面，可以调用`location.assign()`。如果要重新加载当前页面，调用`location.reload()`方法非常方便

### document

`document`对象表示当前页面。由于HTML在浏览器中以DOM形式表示为树形结构，`document`对象就是整个DOM树的根节点

用document对象提供的`getElementById()`和`getElementsByTagName()`可以按`ID`获得一个DOM节点和按`Tag`名称获得一组DOM节点

JavaScript可以通过`document.cookie`读取到当前页面的Cookie,服务器在设置Cookie时可以使用`httpOnly`，设定了`httpOnly`的Cookie将不能被JavaScript读取

### history

`history`对象保存了浏览器的历史记录，JavaScript可以调用`history`对象的`back()`或`forward ()`，相当于用户点击了浏览器的“后退”或“前进”按钮

任何情况，你都不应该使用`history`这个对象了

---

<h1 id="6.2">操作DOM</h1>

当网页被加载时，浏览器会创建页面的文档对象模型（Document Object Model）。

HTML DOM 模型被构造为对象的树。

通过可编程的对象模型，JavaScript 获得了足够的能力来创建动态的 HTML:

- JavaScript 能够改变页面中的所有HTML元素
- JavaScript 能够改变页面中的所有HTML属性
- JavaScript 能够改变页面中的所有 CSS 样式
- JavaScript 能够对页面中的所有事件做出反应

查找HTML元素:

- `document.getElementById()`通过 id 找到HTML元素
- `document.getElementsByTagName()`通过标签名找到HTML元素
- `document.getElementsByClassName()`通过类名找到HTML元素

第二种方法是使用`querySelector()`和`querySelectorAll()`，需要了解selector语法，然后使用条件来获取节点

---

### 更新DOM

改变HTML输出流
JavaScript 能够创建动态的HTML内容：
JavaScript 中，`document.write()`可用于直接向HTML输出流写内容:
    document.getElementById(id).write('text')

改变HTML内容
修改HTML内容的最简单的方法时使用 `innerHTML` 属性。
    document.getElementById(id).innerHTML = newHTML

第二种是修改`innerText`或`textContent`属性，这样可以自动对字符串进行HTML编码，保证无法设置任何HTML标签
    document.getElementById(id).innerText = newText
    document.getElementById(id).textContent = newText

两者的区别在于读取属性时，`innerText`不返回隐藏元素的文本，而`textContent`返回所有文本

改变 HTML 属性
如需改变 HTML 元素的属性，请使用这个语法：
    document.getElementById(id).attribute = newValue

修改CSS也是经常需要的操作。DOM节点的`style`属性对应所有的CSS，可以直接获取或设置。因为CSS允许font-size这样的名称，但它并非JavaScript有效的属性名，所以需要在JavaScript中改写为驼峰式命名fontSize

    document.getElementById(id).style.attribute = newValue

### 插入DOM

一个是使用`appendChild`，把一个子节点添加到父节点的最后一个子节点:
    document.getElementById(id).appendChild(HTML)

动态创建一个节点然后添加到DOM树中:
    document.createElement('tag')

如果我们要把子节点插入到指定的位置怎么办？可以使用:
    parentElement.insertBefore(newElement, referenceElement)

### 删除DOM

要删除一个节点，首先要获得该节点本身以及它的父节点，然后，调用父节点的`removeChild`把自己删掉：
    var self = document.getElementById('to-be-removed');
    var parent = self.parentElement;
    var removed = parent.removeChild(self);
    removed === self; // true

当你遍历一个父节点的子节点并进行删除操作时，要注意，`children`属性是一个只读属性，并且它在子节点变化时会实时更新


---

<h1 id="6.3">操作表单</h1>

用JavaScript操作表单和操作DOM是类似的，因为表单本身也是DOM树

不过表单的输入框、下拉框等可以接收用户输入，所以用JavaScript来操作表单，可以获得用户输入的内容，或者对一个输入框设置新的内

HTML表单的输入控件主要有以下几种：

    文本框，对应的<input type="text">，用于输入文本；
    口令框，对应的<input type="password">，用于输入口令；
    单选框，对应的<input type="radio">，用于选择一项；
    复选框，对应的<input type="checkbox">，用于选择多项；
    下拉框，对应的<select>，用于选择一项；
    隐藏文本，对应的<input type="hidden">，用户不可见，但表单提交时会把隐藏文本发送到服务器。

### 修改值

如果我们获得了一个`<input>`节点的引用，就可以直接调用`value`获得对应的用户输入值。这种方式可以应用于text、password、hidden以及select。但是，对于单选框和复选框，`value`属性返回的永远是HTML预设的值，而我们需要获得的实际是用户是否“勾上了”选项，所以应该用`checked`判断

### 设置值

对于text、password、hidden以及select，直接设置value就可以，
对于单选框和复选框，设置`checked`为`true`或`false`即可

### 提交表单

方式一是通过`<form>`元素的`submit()`方法提交一个表单，例如，响应一个`<button>`的`click`事件，在JavaScript代码中提交表单

第二种方式是响应`<form>`本身的`onsubmit`事件，在提交form时作修改

*注*:要return true来告诉浏览器继续提交，如果return false，浏览器将不会继续提交form

很多登录表单希望用户输入用户名和口令，但是，安全考虑，提交表单时不传输明文口令，而是口令的
     pwd.value = toMD5(pwd.value);


---

<h1 id="6.4">操作文件</h1>

在HTML表单中，可以上传文件的唯一控件就是`<input type="file">`

**注意**：当一个表单包含`<input type="file">`时，表单的`enctype`必须指定为`multipart/form-data`，`method`必须指定为`post`，浏览器才能正确编码并以`multipart/form-dat`a格式发送表单的数据。

HTML5的File API提供了`File`和`FileReader`两个主要对象，可以获得文件信息并读取文件

JavaScript中，执行多任务实际上都是异步调，所以我们在JavaScript代码中就不知道什么时候操作结束，因此需要先设置一个回调函数。当文件读取完成后，JavaScript引擎将自动调用我们设置的回调函数。执行回调函数时，文件已经读取完毕，所以我们可以在回调函数内部安全地获得文件内容


---

<h1 id="6.5">AJAX</h1>

AJAX(Asynchronous JavaScript and XML)异步的JavaScript和XML

AJAX 是一种在无需重新加载整个网页的情况下，能够更新部分网页的技术

AJAX请求是异步执行的，也就是说，要通过回调函数获得响应，在现代浏览器上写AJAX主要依靠`XMLHttpRequest`对象（IE5 和 IE6 使用 ActiveXObject）

    var xmlhttp;
    if (window.XMLHttpRequest){
    xmlhttp=new XMLHttpRequest();
    }else{
    xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
    }

    function success(text) {
        var textarea = document.getElementById('test-response-text');
        textarea.value = text;
    }

    function fail(code) {
        var textarea = document.getElementById('test-response-text');
        textarea.value = 'Error code: ' + code;
    }

    var request = new XMLHttpRequest(); // 新建XMLHttpRequest对象

    request.onreadystatechange = function () { // 状态发生变化时，函数被回调
        if (request.readyState === 4) { // 成功完成
            // 判断响应结果:
            if (request.status === 200) {
                // 成功，通过responseText拿到响应的文本:
                return success(request.responseText);
            } else {
                // 失败，根据响应码判断失败原因:
                return fail(request.status);
            }
        } else {
            // HTTP请求还在继续...
        }
    }

    // 发送请求:
    request.open('GET', '/');
    request.send();

    alert('请求已发送，请等待响应...');

当创建了`XMLHttpRequest`对象后，要先设置`onreadystatechange`的回调函数。在回调函数中，通常我们只需通过`readyState === 4`判断请求是否完成，如果已完成，再根据`status === 200`判断是否是一个成功的响应。

`XMLHttpRequest`对象的`open()`方法有3个参数，第一个参数指定是`GET`还是`POST`，第二个参数指定`URL`地址，第三个参数指定是否使用异步，默认是`true`，所以不用写

最后调用`send()`方法才真正发送请求。`GET`请求不需要参数，`POST`请求需要把`body`部分以字符串或者`FormData`对象传进去

### 安全限制

默认情况下，JavaScript在发送AJAX请求时，URL的域名必须和当前页面完全一致

JavaScript请求外域（就是其他网站）的URL：
一是通过Flash插件发送HTTP请求；
二是通过在同源域名下架设一个代理服务器来转发，JavaScript负责把请求发送到代理服务器：
    '/proxy?url=http://www.sina.com.cn'

第三种方式称为`JSONP`，它有个限制，只能用`GET`请求，并且要求返回JavaScript。这种方式跨域实际上是利用了浏览器允许跨域引用JavaScript资源：

### CORS

如果浏览器支持HTML5，那么就可以一劳永逸地使用新的跨域策略：CORS了。

CORS全称Cross-Origin Resource Sharing，是HTML5规范定义的如何跨域访问资源


---

<h1 id="6.6">Promise</h1>

在JavaScript的世界中，所有代码都是单线程执行的。

由于这个“缺陷”，导致JavaScript的所有网络操作，浏览器事件，都必须是异步执行。异步执行可以用回调函数实现

上一节的AJAX异步执行函数转换为`Promise`对象，看看用`Promise`如何简化异步处理

    // ajax函数将返回Promise对象:
    function ajax(method, url, data) {
        var request = new XMLHttpRequest();
        return new Promise(function (resolve, reject) {
            request.onreadystatechange = function () {
                if (request.readyState === 4) {
                    if (request.status === 200) {
                        resolve(request.responseText);
                    } else {
                        reject(request.status);
                    }
                }
            };
            request.open(method, url);
            request.send(data);
        });
    }
    var log = document.getElementById('test-promise-ajax-result');
    var p = ajax('GET', '/api/categories');
    p.then(function (text) { // 如果AJAX成功，获得响应内容
        log.innerText = text;
    }).catch(function (status) { // 如果AJAX失败，获得响应代码
        log.innerText = 'ERROR: ' + status;
    });

**注**：这段需要重新学习研究

----

----


---

<h1 id="6.7">Canvas</h1>

Canvas是HTML5新增的组件，它就像一块幕布，可以用JavaScript在上面绘制各种图表、动画等

一个Canvas定义了一个指定尺寸的矩形框，在这个范围内我们可以随意绘制：

    <canvas id="test-canvas" width="300" height="200"></canvas>

`getContext('2d')`方法让我们拿到一个`CanvasRenderingContext2D`对象，所有的绘图操作都需要通过这个对象完成
    
    var ctx - canvas.getContext('2d');      //绘制2D
    var gl = canvas.getCOntext('webgl');    //绘制3D

Canvas的坐标系统：

![canvas](images/2017-07-17-1.png)

Canvas除了能绘制基本的形状和文本，还可以实现动画、缩放、各种滤镜和像素转换等高级操作。如果要实现非常复杂的操作，考虑以下优化方案：

- 通过创建一个不可见的`Canvas`来绘图，然后将最终绘制结果复制到页面的可见`Canvas`中；
- 尽量使用整数坐标而不是浮点数；
- 可以创建多个重叠的`Canvas`绘制不同的层，而不是在一个`Canvas`中绘制非常复杂的图；
- 背景图片如果不变可以直接用`<img>`标签并放到最底层。

