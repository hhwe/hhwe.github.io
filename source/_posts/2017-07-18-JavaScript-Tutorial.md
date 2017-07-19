---
title: JavaScript-jQuery
date: 2017-07-18 15:55:56
categories: JS
tags: 
    - JS
    - tutorial
---

*   [jQuery](#7.0)
    *   [选择器](#7.1)
    *   [查找和过滤](#7.2)
    *   [操作DOM](#7.3)
    *   [事件](#7.4)


---

jQuery这么流行，肯定是因为它解决了一些很重要的问题。实际上，jQuery能帮我们干这些事情：

- 消除浏览器差异：你不需要自己写冗长的代码来针对不同的浏览器来绑定事件，编写AJAX等代码；
- 简洁的操作DOM的方法：写`$('#test')`肯定比`document.getElementById('test')`来得简洁；
- 轻松实现动画、修改CSS等各种操作。

jQuery的理念“Write Less, Do More“，让你写更少的代码，完成更多的工作！

`$`是著名的jQuery符号。实际上，jQuery把所有功能全部封装在一个全局变量jQuery中，而`$`也是一个合法的变量名，它是变量jQuery的别名

jQuery语法是为HTML元素的选取编制的，可以对元素执行某些操作。
基础语法是：`$(selector).action()`
- 美元符号`$`定义 jQuery
- 选择符`（selector）`“查询”和“查找” HTML 元素
- jQuery的`action()`执行对元素的操作

---

<h1 id="7.1">选择器<h1>


jQuery元素选择器:使用CSS选择器来选取HTML元素:

    // 查找<p id="demo" class="intro">...</p>:
    $("p") 选取<p>元素。
    $("p.intro") 选取所有class="intro"的<p>元素。
    $("p#demo") 选取所有id="demo"的<p>元素。
    
jQuery属性选择器:使用XPath表达式来选择带有给定属性的元素:

    $("[href]") 选取所有带有href属性的元素。
    $("[href='#']") 选取所有带有href值等于"#"的元素。
    $("p[href='#']") 选取所有带有href值等于"#"的<p>元素。
    $("[href$='.jpg']") 选取所有href值以 ".jpg" 结尾的元素。
    $('[class^="icon-"]')选取所有class值以 "icon-" 结尾的元素

层级选择器:如果两个DOM元素具有层级关系，就可以用`$('ancestor descendant')`来选择，层级之间用空格隔开

    $('ul li');//选择<ul>下的所有的<li>节点

子选择器`$('parent>child'`)类似层级选择器，但是限定了层级关系必须是父子关系，就是`<child>`节点必须是`<parent`>节点的直属子节点

    $('ul>li');//选择<ul>下的所有的<li>子节点

过滤器一般不单独使用，它通常附加在选择器上，帮助我们更精确地定位元素。观察过滤器的效果

    $('ul li:first-child'); // 仅选出第一个元素
    $('ul li:last-child'); // 仅选出最后一个元素
    $('ul li:nth-child(2)'); // 选出第N个元素，N从1开始
    $('ul li:nth-child(even)'); // 选出序号为偶数的元素
    $('ul li:nth-child(odd)'); // 选出序号为奇数的元素

针对表单元素，jQuery还有一组特殊的选择器`:input`，`:file`，`:radio`，`:checkbo`等


---

<h1 id="7.2">查找和过滤<h1>

最常见的查找是在某个节点的所有子节点中查找，使用`find()`方法，它本身又接收一个任意的选择器

    var ul = $('ul'); // 获得<ul>
    var dy = ul.find('.dy'); // 获得<ul>下class='dy'的元素

如果要从当前节点开始向上查找，使用`parent()`方法
    
    var parent = dy.parent();   //获得<ul>
    var a = dy.parent('div.red'); /// 从dy的父节点开始向上查找，直到找到某个符合条件的节点并返回

对于位于同一层级的节点，可以通过`next()`和`prev()`方法

和函数式编程的map、filter类似，jQuery对象也有类似的方法。

`filter()`方法可以过滤掉不符合选择器条件的节点:

    var dy = ul.filter('.dy'); // 获得<ul>下class='dy'的元素

`map()`方法把一个jQuery对象包含的若干DOM节点转化为其他对象:

    var arr = langs.map(function () {
        return this.innerHTML;
    }).get(); // 用get()拿到包含string的Array：['JavaScript', 'Python', 'Swift', 'Scheme', 'Haskell']

此外，一个jQuery对象如果包含了不止一个DOM节点，`first()`、`last()`和`slice()`方法可以返回一个新的jQuery对象，把不需要的DOM节点去掉：

    var langs = $('ul.lang li');
    var js = langs.first(); //相当于$('ul.lang li:first-child')
    var haskell = langs.last(); //相当于$('ul.lang li:last-child')
    var sub = langs.slice(2, 4); //参数和数组的slice()方法一致

---

<h1 id="7.3">操作DOM<h1>

### 修改Text和HTML

jQuery对象的`text()`和`html()`方法分别*获取*和*修改*节点的文本和原始HTML文本

一个jQuery对象可以包含0个或任意个DOM对象，它的方法实际上会作用在对应的每个DOM节点上，这意味着jQuery帮你免去了许多`if`语句

### 修改CSS

调用jQuery对象的`css('name', 'value')`方法,`css()`方法将作用于DOM节点的`style`属性，具有最高优先级。如果要修改class属性，可以用jQuery提供的下列方法：

    var div = $('#test-div');
    div.css('color', '#336699'); // 设置CSS属性
    div.hasClass('highlight'); // false，class是否包含highlight
    div.addClass('highlight'); // 添加highlight这个class
    div.removeClass('highlight'); // 删除highlight这个class

### 显示和隐藏DOM

要隐藏一个DOM，我们可以设置CSS的display属性为none，利用css()方法就可以实现。不过，要显示这个DOM就需要恢复原有的display属性，这就得先记下来原有的display属性到底是block还是inline还是别的值。

考虑到显示和隐藏DOM元素使用非常普遍，jQuery直接提供`show()`和`hide()`方法，我们不用关心它是如何修改display属性的，总之它能正常工作：

    var a = $('a[target=_blank]');
    a.hide(); // 隐藏
    a.show(); // 显示

### 获取DOM信息

`width()`,`height()`获取DOM的宽高等信息，`attr()`和`removeAttr()`方法用于操作DOM节点的属性

`prop()`方法和`attr()`类似，但是HTML5规定有一种属性在DOM节点中可以没有值，只有出现与不出现两种，`attr()`和`prop()`对于属性`checked`处理有所不同，`prop()`返回值更合理一些。不过，用`is()`方法判断更好`is(':checked')`，类似的属性还有`selected`，处理时最好用`is(':selected')`

### 操作表单

对于表单元素，jQuery对象统一提供`val()`方法获取和设置对应的`value`属性


## 修改DOM结构

### 添加DOM

要添加新的DOM节点，除了通过jQuery的`html()`这种暴力方法外，还可以用`append()`方法，除了接受字符串，`append()`还可以传入原始的DOM对象，jQuery对象和函数对象

`append()`把DOM添加到最后，`prepend()`则把DOM添加到最

如果要把新节点插入到指定位置，可以先定位到插入元素前，同级节点可以用`after()`或者`before()`方法

### 删除DOM

要删除DOM节点，拿到jQuery对象后直接调用`remove()`方法就可以了。如果jQuery对象包含若干DOM节点，实际上可以一次删除多个DOM节



---

<h1 id="7.4">事件<h1>

因为JavaScript在浏览器中以单线程模式运行，页面加载后，一旦页面上所有的JavaScript代码被执行完后，就只能依赖触发事件来执行JavaScript代码

浏览器在接收到用户的鼠标或键盘输入后，会自动在对应的DOM节点上触发相应的事件。如果该节点已经绑定了对应的JavaScript处理函数，该函数就会自动调用

`on`方法用来绑定一个事件，我们需要传入事件名称和对应的处理函数,
直接调用`click()`方法：

    $("button").click(function() {..some code... } )


### 鼠标事件

+ click: 鼠标单击时触发；
+ dblclick：鼠标双击时触发；
+ mouseenter：鼠标进入时触发；
+ mouseleave：鼠标移出时触发；
+ mousemove：鼠标在DOM内部移动时触发；(chrome上有问题)
+ hover：鼠标进入和退出时触发两个函数，相当于mouseenter加上mouseleave。

### 键盘事件

键盘事件仅作用在当前焦点的DOM上，通常是`<input>`和`<textarea>`。

+ keydown：键盘按下时触发；
+ keyup：键盘松开时触发；
+ keypress：按一次键后触发。


### 其他事件

+ focus：当DOM获得焦点时触发；
+ blur：当DOM失去焦点时触发；
+ change：当`<input>`、`<select`>或`<textarea>`的内容改变时触发；
+ submit：当`<form>`提交时触发；
+ ready：当页面被载入并且DOM树完成初始化后触发,仅作用于`document`对象

我们自己的初始化代码必须放到`document`对象的`ready`事件中，保证DOM已完成初始化:
    $(document).ready(function(){
        ...
    });

如果你遇到`$(function () {...})`的形式，牢记这是document对象的ready事件处理函数

### 事件参数

有些事件，如`mousemove`和`keypress`，我们需要获取鼠标位置和按键的值，否则监听这些事件就没什么意义了。所有事件都会传入Event对象作为参数，可以从Event对象上获取到更多的信息：

### 取消绑定

无参数调用`off()`一次性移除已绑定的所有类型的事件处理函数，一个已被绑定的事件可以解除绑定，通过`off('click', function)`实现

`input.change()`相当于`input.trigger('change')`，它是`trigger()`方法的简写


---

<h1 id="7.5">动画<h1>

用JavaScript实现动画，原理非常简单：我们只需要以固定的时间间隔（例如，0.1秒），每次把DOM元素的CSS样式修改一点（例如，高宽各增加10%），看起来就像动画了

### show/hide

直接以无参数形式调用`show()`和`hide()`，会显示和隐藏DOM元素，`toggle()`方法则根据当前状态决定是`show()`还是`hide()`。但是，只要传递一个时间参数进去，就变成了动画

### slideUp/slideDown

`slideUp()`把一个可见的DOM元素收起来，效果跟拉上窗帘似的，`slideDown()`相反，而`slideToggle()`则根据元素是否可见来决定下一步动作

### fadeIn/fadeOut

`fadeIn()`和`fadeOut()`的动画效果是淡入淡出，也就是通过不断设置DOM元素的`opacity`属性来实现，而`fadeToggle(`)则根据元素是否可见来决定下一步动作

### 自定义动画

`animate()`，它可以实现任意动画效果，我们需要传入的参数就是DOM元素最终的CSS状态和时间，jQuery在时间段内不断调整CSS直到达到我们设定的值


---

<h1 id="7.6">AJAX<h1>

jQuery在全局对象`jQuery`（也就是`$`）绑定了`ajax(`)函数，可以处理AJAX请求。`ajax(url, settings)`函数需要接收一个`UR`L和一个可选的`settings`对象，常用的选项如下：

- `async`：是否异步执行AJAX请求，默认为true，千万不要指定为false；
- `method`：发送的Method，缺省为'GET'，可指定为'POST'、'PUT'等；
- `contentTyp`e：发送POST请求的格式，默认值为`'application/x-www-form-urlencoded; charset=UTF-8'`，也可以指定为`text/plain`、`application/json`；
- `data`：发送的数据，可以是字符串、数组或object。如果是GET请求，data将被转换成query附加到URL上，如果是POST请求，根据contentType把data序列化成合适的格式；
- `headers`：发送的额外的HTTP头，必须是一个object；
- `dataType`：接收的数据格式，可以指定为'html'、'xml'、'json'、'text'等，缺省情况下根据响应的Content-Type猜测。

下面的例子发送一个GET请求，并返回一个JSON格式的数据：

    var jqxhr = $.ajax('/api/categories', {
        dataType: 'json'
    });

对常用的AJAX操作，jQuery提供了一些辅助方法。由于GET请求最常见，所以jQuery提供了`get()`方法，可以这么写
    
    var jqxhr = $.get('/path/to/resource', {
        name: 'Bob Lee',
        check: 1
    }); //'/path/to/resource?name=Bob%20Lee&check=1'

`post()`和`get()`类似，但是传入的第二个参数默认被序列化为`application/x-www-form-urlencoded`

    var jqxhr = $.post('/path/to/resource', {
        name: 'Bob Lee',
        check: 1
    }); // 'name=Bob%20Lee&check=1'作为POST的body被发送

`getJSON()`方法来快速通过GET获取一个JSON对象


---

<h1 id="7.7">扩展<h1>


当我们使用jQuery对象的方法时，由于jQuery对象可以操作一组DOM，而且支持链式操作，所以用起来非常方便。

但是jQuery内置的方法永远不可能满足所有的需求。比如，我们想要高亮显示某些DOM元素，用jQuery可以这么实现：

    $('span.hl').css('backgroundColor', '#fffceb').css('color', '#d85030');
    $('p a.hl').css('backgroundColor', '#fffceb').css('color', '#d85030');

我们可以扩展jQuery来实现自定义方法。将来如果要修改高亮的逻辑，只需修改一处扩展代码。这种方式也称为编写jQuery插件

给jQuery对象绑定一个新方法是通过扩展`$.fn`对象实现的。让我们来编写第一个扩展——`highlight1()`:

    $.fn.highlight1 = function(){
        this.css('backgroundColor', '#fffceb').css('color', '#d85030');
        return this;
    }

细心的童鞋可能发现了，为什么最后要`return this;`？因为jQuery对象支持链式操作，我们自己写的扩展方法也要能继续链式下去

    $.fn.highlight2 = function(options){
        var bgcolor = options && options.backgroundColor || '#fffceb';
        var color = options && options.color || 'd85030';
        this.css('backgroundColor', bgcolor).css('color', color);
        return this;
    }

对于默认值的处理，我们用了一个简单的`&&`和`||`短路操作符，总能得到一个有效的值。另一种方法是使用jQuery提供的辅助方法`$.extend(target, obj1, obj2, ...)`，它把多个object对象的属性合并到第一个target对象中，遇到同名属性，总是使用靠后的对象的值，也就是越往后优先级越高：

    $.fn.highlight = function (options) {
        var opts = $.extend({}, $.fn.highlight.defaults, options);
        this.css('backgroundColor', opts.backgroundColor).css('color', opts.color);
        return this;
    }
    $.fn.highlight.defaults = {
        color: '#d85030',
        backgroundColor: '#fff8de'
    }

最终，我们得出编写一个jQuery插件的原则：

- 给`$.fn`绑定函数，实现插件的代码逻辑；
- 插件函数最后要`return this;`以支持链式调用；
- 插件函数要有默认值，绑定在`$.fn.<pluginName>.defaults`上；
- 用户在调用时可传入设定值以便覆盖默认值。


