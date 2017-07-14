---
title: JavaScript-函数
date: 2017-07-14 22:17:39
categories: JS
tags: 
    - JS
    - tutorial
---

# 目录

*   [函数](#3.0)  
    *   [函数定义和调用](#3.1)
    *   [变量作用域](#3.2)
    *   [方法](#3.3)
    *   [高阶函数](#3.4)
    *   [闭包](#3.5)
    *   [箭头函数](#3.6)
    *   [generator](#3.7)

---


<h1 id="3.0">函数</h1>

---

<h2 id="3.1">函数定义和调用</h2>

### 定义函数

在JavaScript中，定义函数的方式如下：

    function name(x) {
        ...
    }

`function`指出这是一个函数定义；
`name`是函数的名称；
`(x)`括号内列出函数的参数，多个参数以`,`分隔；
`{ ... }`之间的代码是函数体，可以包含若干语句，甚至可以没有任何语句。

*注*：如果没有`return`语句，函数执行完毕后也会返回结果，只是结果为undefined。

由于JavaScript的函数也是一个对象，上述定义的函数实际上是一个函数对象，而函数名`name`可以视为指向该函数的变量。

因此，第二种定义函数的方式如下：

    var name = function (x) {
        ...
    };

在这种方式下，function (x) { ... }是一个匿名函数，它没有函数名。但是，这个匿名函数赋值给了变量name，所以，通过变量name就可以调用该函数。

上述两种定义完全等价，注意第二种方式按照完整语法需要在函数体末尾加一个`;`，表示赋值语句结束。

### 调用函数

由于JavaScript允许传入任意个参数而不影响调用，因此传入的参数比定义的参数多也没有问题，虽然函数内部并不需要这些参数

传入的参数比定义的少也没有问题：

    abs(); // 返回NaN
    
此时abs(x)函数的参数x将收到undefined，计算结果为NaN。

- argument
JavaScript还有一个免费赠送的关键字`arguments`，它只在函数内部起作用，并且永远指向当前函数的调用者传入的所有参数。也就是说，即使函数不定义任何参数，还是可以拿到参数的值
- rest
`rest`参数只能写在最后，前面用`...`标识，从运行结果可知，传入的参数先绑定`a`、`b`，多余的参数以数组形式交给变量`rest`，所以，不再需要`arguments`我们就获取了全部参数。如果传入的参数连正常定义的参数都没填满，也不要紧，`rest`参数会接收一个空数组（注意不是undefined）。

*注*：前面我们讲到了JavaScript引擎有一个在行末自动添加分号的机制，这可能让你栽到return语句的一个大坑

---

<h2 id="3.2">变量作用域</h2>

在JavaScript中，用`var`申明的变量实际上是有作用域的。

### 变量提升

JavaScript的函数定义有个特点，它会先扫描整个函数体的语句，把所有申明的变量“提升”到函数顶部：

    'use strict';
    function foo() {
        var x = 'Hello, ' + y;  
        alert(x);   // 没有报错输出'Hello, undefined'
        var y = 'Bob';  //变量y`提升`了
    }
    foo();

由于JavaScript的这一怪异的“特性”，我们在函数内部定义变量时，请严格遵守“在函数内部首先申明所有变量”这一规则。

### 全局作用域

不在任何函数内定义的变量就具有全局作用域。实际上，JavaScript默认有一个全局对象window，全局作用域的变量实际上被绑定到window的一个属性：

    var c = '1';    //相当于window.c = '1';
    var f = foo(){} //相当于window.f = f();


全局变量会绑定到window上，不同的JavaScript文件如果使用了相同的全局变量，或者定义了相同名字的顶层函数，都会造成命名冲突，并且很难被发现。减少冲突的一个方法是把自己的所有变量和函数全部绑定到一个全局变量中。例如：

    // 唯一的全局变量MYAPP:
    var MYAPP = {};
    // 其他变量:
    MYAPP.name = 'myapp';
    MYAPP.version = 1.0;
    // 其他函数:
    MYAPP.foo = function () {
        return 'foo';
    };

### 局部作用域

如果一个变量在函数体内部申明，则该变量的作用域为整个函数体，在函数体外不可引用该变量。由于JavaScript的函数可以嵌套，此时，内部函数可以访问外部函数定义的变量，反过来则不行

由于JavaScript的变量作用域实际上是函数内部，我们在`for`循环等语句块中是无法定义具有局部作用域的变量的。为了解决块级作用域，ES6引入了新的关键字`let`，用`let`替代`var`可以申明一个块级作用域的变量：

### 常量

由于`var`和`let`申明的是变量，如果要申明一个常量，在ES6之前是不行的，我们通常用全部大写的变量来表示“这是一个常量，不要修改它的值”：

    var PI = 3.14;

ES6标准引入了新的关键字`const`来定义常量，`const`与`let`都具有块级作用域：

    'use strict';
    const PI = 3.14;
    PI = 3;
    PI //3.14

**【补充】**：
    const   常量
    let     变量，块作用域，不能重复声明覆盖
    var     变量，函数作用域，能重复声明覆盖

赋值之后不会再做修改了就用const，如果后边还会修改就用let，不建议使用var

---

<h2 id="3.3">方法</h2>

### this

在JavaScript中，对象的定义是这样的：

    var xiaoming = {
        name: '小明',
        birth: 1990,
        age: function () {
            var y = new Date().getFullYear();
            return y - this.birth;
        }
    };

绑定到对象上的函数称为方法，和普通函数也没啥区别，但是它在内部使用了一个`this`关键字，在一个方法内部，`this`是一个特殊变量，它始终指向当前对象，也就是xiaoming这个变量。

让我们拆开写：

    function getAge() {
        var y = new Date().getFullYear();
        return y - this.birth;
    }
    var xiaoming = {
        name: '小明',
        birth: 1990,
        age: getAge
    };
    xiaoming.age(); // 25, 正常结果
    getAge(); // NaN, 若在strict模式下将得到一个错误

如果以对象的方法形式调用，比如`xiaoming.age()`，该函数的`this`指向被调用的对象，也就是`xiaoming`，这是符合我们预期的。

如果单独调用函数，比如`getAge()`，此时，该函数的`this`指向全局对象，也就是`window`。

由于这是一个巨大的设计错误，要想纠正可没那么简单。ECMA决定，在`strict`模式下让函数的`this`指向`undefined`，因此，在`strict`模式下，你会得到一个错误.

### apply

要指定函数的this指向哪个对象，可以用函数本身的`apply`方法，它接收两个参数，第一个参数就是需要绑定的`this`变量，第二个参数是`Array`，表示函数本身的参数。

用`apply`修复`getAge()`调用：

    getAge.apply(xiaoming, []); // 25, this指向xiaoming, 参数为空

另一个与`apply()`类似的方法是`call()`，唯一区别是：`apply()`把参数打包成Array再传入；`call()`把参数按顺序传入。

比如调用`Math.max(3, 5, 4`)，分别用`apply()`和`call()`实现如下：

    Math.max.apply(null, [3, 5, 4]); // 5
    Math.max.call(null, 3, 5, 4); // 5

---

<h2 id="3.4">高阶函数</h2>

函数就可以接收另一个函数作为参数，这种函数就称之为高阶函数

### map

`map()`方法定义在JavaScript的Array中，我们调用Array的`map()`方法，传入我们自己的函数，就得到了一个新的Array作为结果

### reduce

Array的`reduce()`把一个函数作用在这个Array的`[x1, x2, x3...]`上，这个函数必须接收两个参数，`reduce()`把结果继续和序列的下一个元素做累积计算

### filter

Array的`filter()`也接收一个函数。和`map()`不同的是，`filter()`把传入的函数依次作用于每个元素，然后根据返回值是`true`还是`false`决定保留还是丢弃该元素。通常我们仅使用第一个参数，表示Array的某个元素，还可以接收另外两个参数，表示元素的位置和数组本身

### sort

Array的`sort()`方法默认把所有元素先转换为`String`再排序:

    [10, 20, 1, 2].sort(); // [1, 10, 2, 20]

`sort()`方法也是一个高阶函数，它还可以接收一个比较函数来实现自定义的排序。要按数字大小排序，我们可以自建函数

---

<h2 id="3.5">闭包</h2>

高阶函数除了可以接受函数作为参数外，还可以把函数作为结果值返回。

需要注意的问题是，返回的函数并没有立刻执行，而是直到调用了`f()`才执行。我们来看一个例子：

    function count() {
        var arr = [];
        for (var i=1; i<=3; i++) {
            arr.push(function () {
                return i * i;
            });
        }
        return arr;
    }

    var results = count();
    var f1 = results[0];
    var f2 = results[1];
    var f3 = results[2];

在上面的例子中，每次循环，都创建了一个新的函数，然后，把创建的3个函数都添加到一个Array中返回了。

你可能认为调用f1()，f2()和f3()结果应该是1，4，9，但实际结果是：

    f1(); // 16
    f2(); // 16
    f3(); // 16

全部都是16！原因就在于返回的函数引用了变量i，但它并非立刻执行。等到3个函数都返回时，它们所引用的变量i已经变成了4，因此最终结果为16。

返回闭包时牢记的一点就是：返回函数不要引用任何循环变量，或者后续会发生变化的变量。

---

<h2 id="3.6">箭头函数</h2>

ES6标准新增了一种新的函数：`Arrow Function`（箭头函数）。为什么叫`Arrow Function`？因为它的定义用的就是一个箭头：

    x => x * x

上面的箭头函数相当于：

    function (x) {
        return x * x;
    }

箭头函数相当于匿名函数，并且简化了函数定义。箭头函数有两种格式，一种像上面的，只包含一个表达式，连`{ ... }`和return都省略掉了。还有一种可以包含多条语句，这时候就不能省略`{ ... }`和`return`：

    x => {
        ...
    }

如果参数不是一个，就需要用括号`()`括起来：

    (x, y) => x * x + y * y

箭头函数看上去是匿名函数的一种简写，但实际上，箭头函数和匿名函数有个明显的区别：箭头函数内部的`this`是词法作用域，由上下文确定

    var obj = {
        birth: 1990,
        getAge: function () {
            var b = this.birth; // 1990
            var fn = () => new Date().getFullYear() - this.birth; // this指向obj对象
            return fn();
        }
    };
    obj.getAge(); // 25

---

<h2 id="3.7">generator</h2>

`generator`（生成器）是ES6标准引入的新的数据类型。一个`generator`看上去像一个函数，但可以返回多次。

函数在执行过程中，如果没有遇到`return`语句（函数末尾如果没有`return`，就是隐含的`return undefined`;），控制权无法交回被调用的代码。`generator`和函数不同的是，`generator`由`function*`定义（注意多出的*号），并且，除了`return`语句，还可以用`yield`返回多次。

    function* fib(max) {
        var
            t,
            a = 0,
            b = 1,
            n = 1;
        while (n < max) {
            yield a;
            t = a + b;
            a = b;
            b = t;
            n ++;
        }
        return a;
    }

调用`generator`对象有两个方法，一是不断地调用`generator`对象的`next()`方法

    var f = fib(1);
    f.next(); // {value: 0, done: false} //每次遇到`yield x`;就返回一个对象`{value: x, done: true/false}`
    f.next(); // {value: 1, done: done}
    f.next(); // {value: undefine, done: done} //最后返回一个undefined

第二个方法是直接用`for ... of`循环迭代`generator`对象，这种方式不需要我们自己判断done：

    for (var x of fib(5)) {
        console.log(x); // 依次输出0, 1, 1, 2, 3
    }

function* next_id() {
    for (let i=1; i<1000; i++){
        yield i;
    }
}