---
title: JavaScript-快速入门
date: 2017-07-09 21:24:51
categories: JS
tags: 
    - JS
    - tutorial
---

JS这块学的比较杂，希望能够自己在整理一遍，博客完全是根据
**[W3school](http://www.w3school.com.cn/js/)** 和 **[廖雪峰JavaScript教程](http://www.liaoxuefeng.com/wiki/001434446689867b27157e896e74d51a89c25cc8b43bdb3000)**总结完成的

---

# 目录

**JavaScript教程**

*   [JavaScript简介](#1.0)
*   [快速入门](#2.0)
    *   [基本语法](#2.1)
    *   [数据类型和变量](#2.2)
    *   [字符串](#2.3)
    *   [数组](#2.4)
    *   [对象](#2.5)
    *   [条件判断](#2.6)
    *   [循环](#2.7)
    *   [Map和Set](#2.8)
    *   [iterable](#2.9)


---

<h1 id="1.0">JavaScript简介</h1>


JavaScript一种直译式脚本语言，是一种动态类型、弱类型、基于原型的语言，内置支持类型。它的解释器被称为JavaScript引擎，为浏览器的一部分，广泛用于客户端的脚本语言，最早是在HTML（标准通用标记语言下的一个应用）网页上使用，用来给HTML网页增加动态功能。

### 基本特性
 
1. 是一种解释性脚本语言（代码不进行预编译）。 
2. 主要用来向HTML（标准通用标记语言下的一个应用）页面添加交互行为。 
3. 可以直接嵌入HTML页面，但写成单独的js文件有利于结构和行为的分离。
4. 跨平台特性，在绝大多数浏览器的支持下，可以在多种平台下运行（如Windows、Linux、Mac、Android、iOS等）。
5. JavaScript语言中采用的是弱类型的变量类型,对使用的数据类型未做出严格的要求,是基于Java基本语句和控制的脚本语言,其设计简单紧凑。
6. 动态性。JavaScript是一种采用事件驱动的脚本语言,它不需要经过Web服务器就可以对用户的输入做出响应。在访问一个网页时,鼠标在网页中进行鼠标点击或上下移、窗口移动等操作JavaScript都可直接对这些事件给出相应的响应。

Javascript脚本语言同其他语言一样，有它自身的基本数据类型，表达式和算术运算符及程序的基本程序框架。Javascript提供了四种基本的数据类型和两种特殊数据类型用来处理数据和文字。而变量提供存放信息的地方，表达式则可以完成较复杂的信息处理。

### 日常用途

JavaScript是一种属于网络的脚本语言,已经被广泛用于Web应用开发,常用来为网页添加各式各样的动态功能,为用户提供更流畅美观的浏览效果。通常JavaScript脚本是通过嵌入在HTML中来实现自身的功能的。

1. 嵌入动态文本于HTML页面。 
2. 对浏览器事件做出响应。 
3. 读写HTML元素。 
4. 在数据被提交到服务器之前验证数据。 
5. 检测访客的浏览器信息。 
6. 控制cookies，包括创建和修改等。 
7. 基于Node.js技术进行服务器端编程。

### JS实现

HTML 中的脚本必须位于 `<script>` 与 `</script>` 标签之间。
脚本可被放置在 HTML 页面的 `<body>` 和 `<head>` 部分中。（最好放在body底部）

---

# 快速入门


<h2 id="2.1">基本语法</h2>

### 语法

JavaScript的语法和Java语言类似，每个语句以`;`结束，语句块用`{...}`。但是，JavaScript并不强制要求在每个语句的结尾加`;`，浏览器中负责执行JavaScript代码的引擎会自动在每个语句的结尾补上;

*注意*：让JavaScript引擎自动加分号在某些情况下会改变程序的语义，导致运行结果与期望不一致。在本教程中，我们不会省略`;`，所有语句都会添加`;`。

### 注释

以`//`开头直到行末的字符被视为行注释，用`/*...*/`把多行字符包裹起来，把一大“块”视为一个注释

--------

<h2 id="2.2">数据类型和变量</h2>

### 数据类型

1. **Nndefined**:
    - 在使用var声明变量，但未对其加以初始化时，这个变量的类型就是undefined，且其默认初始化值为undefined。
    - 对未声明与初始化的变量，直接使用，那么这个变量的类型也是undefined，但是没有默认初始化值。
2. **Null**:null类型的默认值是null，从逻辑角度讲，是表示一个空对象指针。可以通过将变量的值设置为 null 来清空变量。
3. **Boolean**:即布尔类型，该类型有两个值：true false
4. **Number**:JavaScript不区分整数和浮点数，统一用Number表示，
    1. 整数,可以通过十进制，八进制，十六进制的字面值来表示。  
    2. 浮点数
    3. NaN,即非数值，是一个特殊的值，这个数值用于表示一个本来要返回数值的操作数，未返回数值的情况。
5. **String**:字符串类型是最熟悉不过的啦，至于用单引号，还是双引号，在js中还是没有差别的。记得成对出现。
6. **Object**:JavaScript的对象是一组由键-值组成的无序集合。JavaScript对象的键都是字符串类型，值可以是任意数据类型。该类型实例化的对象，是一组数据和功能（函数）的集合。

### 变量、运算符

第一种是`==`比较：它会自动转换数据类型再比较，很多时候，会得到非常诡异的结果；

第二种是`===`比较：它不会自动转换数据类型，如果数据类型不一致，返回false，如果一致，再比较。

由于JavaScript这个设计缺陷，不要使用==比较，始终坚持使用===比较。

另一个例外是NaN这个特殊的Number与所有其他值都不相等，包括它自己：

    NaN === NaN; // false

唯一能判断NaN的方法是通过isNaN()函数：

    isNaN(NaN); // true

变量在JavaScript中就是用一个变量名表示，变量名是`大小写英文、数字、$和_的组合`，且不能用数字开头。

### strict模式

如果一个变量没有通过var申明就被使用，那么该变量就自动被申明为全局变量。

    i = 10；//i现在是全局变量

在同一个页面的不同的JavaScript文件中，如果都不用var申明，恰好都使用了变量i，将造成变量i互相影响，产生难以调试的错误结果。

使用var申明的变量则不是全局变量，它的范围被限制在该变量被申明的函数体内（函数的概念将稍后讲解），同名变量在不同的函数体内互不冲突。

为了修补JavaScript这一严重设计缺陷，ECMA在后续规范中推出了strict模式，在strict模式下运行的JavaScript代码，强制通过var申明变量，未使用var申明变量就使用的，将导致运行错误。

启用strict模式的方法是在JavaScript代码的第一行写上：

    'use strict';

---

<h2 id="2.3">字符串</h2>

JavaScript的字符串就是用''或""括起来的字符表示
由于多行字符串用\n写起来比较费事，所以最新的ES6标准新增了一种多行字符串的表示方法，用反引号 \` ... \` 表示

要把多个字符串连接起来，可以用+号连接

    var name = '小明';
    var age = 20;
    var message = '你好, ' + name + ', 你今年' + age + '岁了!';
    alert(message);

ES6新增了一种模板字符串，表示方法和上面的多行字符串一样，但是它会自动替换字符串中的变量：

    var message = `你好, ${name}, 你今年${age}岁了!`;

1. `length`：字符串长度，指定字符可用s[i]，与Array操作相似，但是字符串是不可变的
2. `toUpperCase()、toLowerCase()`将字符串转换大小写
3. `indexOf()`会搜索指定字符串出现的位置
4. `substring()`返回指定索引区间的子串

---

<h2 id="2.4">数组</h2>

JavaScript的Array可以包含任意数据类型，并通过索引来访问每个元素
要取得Array的长度，直接访问length属性：
**注意**:直接给Array的length赋一个新的值会导致Array大小的变化

1. Array也可以通过`indexOf()`来搜索一个指定的元素的位置
2. `slice()`就是对应String的`substring()`版本，它截取Array的部分元素，然后返回一个新的Array
3. `push()`向Array的末尾添加若干元素，`pop()`则把Array的最后一个元素删除掉
4. 如果要往Array的头部添加若干元素，使用`unshift()`方法，`shift()`方法则把Array的第一个元素删掉
5. `sort()`可以对当前Array进行排序，它会直接修改当前Array的元素位置，直接调用时，按照默认顺序排序
6. `reverse()`把整个Array的元素给掉个个，也就是反转
7. `splice()`方法是修改Array的“万能方法”，它可以从指定的索引开始删除若干元素，然后再从该位置添加若干元素
8. `concat()`方法把当前的Array和另一个Array连接起来，并返回一个新的Array
9. `join()`方法是一个非常实用的方法，它把当前Array的每个元素都用指定的字符串连接起来，然后返回连接后的字符串

---

<h2 id="2.5">对象</h2>

JavaScript的对象是一种无序的集合数据类型，它由若干键值对组成。

JavaScript用一个`{...}`表示一个对象，键值对以`xxx: xxx`形式申明，用,隔开。注意，最后一个键值对不需要在末尾加,，如果加了，有的浏览器（如低版本的IE）将报错

    var person = {
        name: 'x',
        birth: 1990,
        school: 'shu',
        height: 1.70,
        weight: 65,
        score: null
    };

实际上JavaScript对象的所有属性都是字符串，不过属性对应的值可以是任意数据类型。

如果访问一个不存在的属性会返回什么呢？JavaScript规定，访问不存在的属性不报错，而是返回`undefined`。由于JavaScript的对象是动态类型，你可以自由地给一个对象添加或删除属性：

    person.age  //undefined
    person.age = 12 
    delete person.age

如果我们要检测xiaoming是否拥有某一属性，可以用`in`操作符:

    'name' in person;     //true
    'grade' in person;     //false

要判断一个属性是否是xiaoming自身拥有的，而不是继承得到的，可以用`hasOwnProperty()`方法

---

<h2 id="2.6">条件判断</h2>

JavaScript使用`if () { ... } else { ... }`来进行条件判断，其中`else`语句是可选的。

JavaScript把`null`、`undefined`、`0`、`NaN`和空字符串`''`视为`false`，其他值一概视为`true`

    `true` == true  //false

在转换不同的数据类型时，相等或者不相等应遵循一下几条规则：

1. 如果有一个操作数是布尔值，则在比较相等之前将其转换为数值--`false`转换为`0`，`true`转换为`1`；
2. 如果一个操作数是字符串，另一个操作符是数值，则在比较相等之前先讲字符串转换为数值；
3. 如果一个操作数是对象，另一个操作数不是，则调用对象的valueOf()方法，用得到的基本类型值按照前面的规则进行比较。

回到这个题目中，根据规则1，先将布尔值转换为数值`1`，变换为字符串和数值的比较。再根据规则2，将字符串转为数值`NaN`。显然不等。

---

<h2 id="2.7">循环</h2>

JavaScript的循环有两种，一种是`for`循环，通过初始条件、结束条件和递增条件来循环执行语句块

`for`循环的3个条件都是可以省略的，如果没有退出循环的判断条件，就必须使用break语句退出循环，否则就是死循环

`for`循环的一个变体是`for ... in`循环，它可以把一个对象的所有属性依次循环出来:

    var o = {
        name: 'Jack',
        age: 20,
        city: 'Beijing'
    };
    for (var key in o) {
        alert(key); // 'name', 'age', 'city'
    }

*注*：`for ... in`对Array的循环得到的是String而不是Numbe

`while`循环只有一个判断条件，条件满足，就不断循环，条件不满足时则退出循环。

最后一种循环是`do { ... } while()`循环，它和`while`循环的唯一区别在于，不是在每次循环开始的时候判断条件，而是在每次循环完成的时候判断条件

---

<h2 id="2.8">Map和Set</h2>

JavaScript的默认对象表示方式`{}`可以视为其他语言中的`Map`或`Dictionary`的数据结构，即一组键值对,但是JavaScript的对象有个小问题，就是键必须是字符串。但实际上Number或者其他数据类型作为键也是非常合理的。为了解决这个问题，最新的ES6规范引入了新的数据类型Map。

### Map

`Map`是一组键值对的结构，具有极快的查找速度。用JavaScript写一个`Map`如下：

    var m = new Map([['Michael', 95], ['Bob', 75], ['Tracy', 85]]);
    m.get('Michael'); // 95

初始化`Map`需要一个二维数组，或者直接初始化一个空`Map`。`Map`具有以下方法：

    var m = new Map(); // 空Map
    m.set('Adam', 67); // 添加新的key-value
    m.set('Bob', 59);
    m.has('Adam'); // 是否存在key 'Adam': true
    m.get('Adam'); // 67
    m.delete('Adam'); // 删除key 'Adam'
    m.get('Adam'); // undefined

### Set

`Set`和`Map`类似，也是一组key的集合，但不存储value。由于key不能重复，所以，在`Set`中，没有重复的key。要创建一个Set，需要提供一个Array作为输入，或者直接创建一个空Set：

    var s1 = new Set(); // 空Set
    var s2 = new Set([1, 2, 3]); // 含1, 2, 3

重复元素在Set中自动被过滤：

    var s = new Set([1, 2, 3, 3, '3']);
    s; // Set {1, 2, 3, "3"}

通过`add(key)`方法可以添加元素到Set中，可以重复添加，但不会有效果。
通过`delete(key)`方法可以删除元素

---

<h2 id="2.9">iterable</h2>

遍历Array可以采用下标循环，遍历Map和Set就无法使用下标。为了统一集合类型，ES6标准引入了新的iterable类型，Array、Map和Set都属于iterable类型。具有iterable类型的集合可以通过新的`for ... of`循环来遍历。

`for ... in`循环将把name包括在内，但Array的length属性却不包括在内:

    var a = ['A', 'B', 'C'];
    a.name = 'Hello';
    for (var x in a) {
        alert(x); // '0', '1', '2', 'name'
    }

`for ... of`循环则完全修复了这些问题，它只循环集合本身的元素：

    var a = ['A', 'B', 'C'];
    a.name = 'Hello';
    for (var x of a) {
        alert(x); // 'A', 'B', 'C'
    }

然而，更好的方式是直接使用iterable内置的`forEach`方法，它接收一个函数，每次迭代就自动回调该函数。以Array为例:

    var a = ['A', 'B', 'C'];
    a.forEach(function (element, index, array) {
        // element: 指向当前元素的值
        // index: 指向当前索引
        // array: 指向Array对象本身
        alert(element);
    });

Set与Array类似，但Set没有索引，因此回调函数的前两个参数都是元素本身:
Map的回调函数参数依次为value、key和map本身

---
