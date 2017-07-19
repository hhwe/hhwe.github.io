---
title: JavaScript-Underscore
date: 2017-07-19 21:50:26
categories: JS
tags: 
    - JS
    - tutorial
---


# underscore

JavaScript是函数式编程语言，支持高阶函数和闭包。函数式编程非常强大，可以写出非常简洁的代码

Array有`map()`和`filter()`方法，可是Object没有这些方法。此外，低版本的浏览器例如IE6～8也没有这些方法，怎么办？

方法一，自己把这些方法添加到`Array.prototype`中，然后给O`bject.prototype`也加上`mapObject()`等类似的方法。

方法二，直接找一个成熟可靠的第三方开源库，使用统一的函数来实现`map()`、`filter()`这些操作。

采用方法二，选择的第三方库就是`underscore`，它提供了一套完善的函数式编程的接口，让我们更方便地在JavaScript中实现函数式编程。

`jQuery`在加载时，会把自身绑定到唯一的全局变量`$`上，`underscore`与其类似，会把自身绑定到唯一的全局变量`_`上，这也是为啥它的名字叫underscore的原因

underscore为集合类对象提供了一致的接口。集合类是指Array和Object，暂不支持Map和Set

## Collections

### map/filter

和Array的`map()`与`filter(`)类似，但是underscore的`map()`和`filter()`可以作用于Object。当作用于Object时，传入的函数为`function (value, key)`，第一个参数接收value，第二个参数接收key

Object作`_.map()`操作的返回结果是Array,`_.mapObject()`返回对象

### every / some

当集合的所有元素都满足条件时，`_.every()`函数返回true，当集合的至少一个元素满足条件时，`_.some()`函数返回true