---
title: JavaScript-Node.js
date: 2017-07-20 13:02:32
categories: JS
tags: 
    - JS
    - tutorial
---

**Node.js**

* [模块](#1.0)
    * [模块](1.1)
    * [模块]()
    * [模块]()
    * [模块]()


---

# 模块

要在模块中对外输出变量，用：

    module.exports = variable;

输出的变量可以是任意对象、函数、数组等等。

要引入其他模块输出的对象，用：

    var foo = require('other_module');

引入的对象具体是什么，取决于引入模块输出的对象。

如果要输出一个键值对象`{}`，可以利用`exports`这个已存在的空对象`{}`，并继续在上面添加新的键值；

    exports.foo = function () { return 'foo'; };
    exports.bar = function () { return 'bar'; };
    module.exports.foo = function () { return 'foo'; };
    module.exports.bar = function () { return 'bar'; };

如果要输出一个函数或数组，必须直接对`module.exports`对象赋值。

所以我们可以得出结论：直接对`module.exports`赋值，可以应对任何情况

## 