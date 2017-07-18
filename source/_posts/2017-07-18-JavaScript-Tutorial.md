---
title: 2017-07-18-JavaScript-Tutorial
date: 2017-07-18 15:55:56
categories: JS
tags: 
    - JS
    - tutorial
---

*   [jQuery](#7.0)
    *   [选择器](#7.1)


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

<h1 id="7.4">操作DOM<h1>
