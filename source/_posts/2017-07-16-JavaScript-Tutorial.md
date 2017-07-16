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

