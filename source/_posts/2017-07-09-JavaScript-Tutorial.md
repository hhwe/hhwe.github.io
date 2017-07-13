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
*   [函数](#3.0)  
    *   [函数定义和调用](#3.1)
    *   [变量作用域](#3.2)
    *   [方法](#3.3)
    *   [高阶函数](#3.4)
    *   [闭包](#3.5)
    *   [箭头函数](#3.6)
    *   [generator](#3.7)
*   [标准对象](#4.0)  


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

HTML 中的脚本必须位于 <script> 与 </script> 标签之间。
脚本可被放置在 HTML 页面的 <body> 和 <head> 部分中。
（最好放在body底部）

---

<h1 id="2.0">快速入门</h1>

---

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

### 字符串定义

JavaScript的字符串就是用''或""括起来的字符表示
由于多行字符串用\n写起来比较费事，所以最新的ES6标准新增了一种多行字符串的表示方法，用反引号 \` ... \` 表示

要把多个字符串连接起来，可以用+号连接

    var name = '小明';
    var age = 20;
    var message = '你好, ' + name + ', 你今年' + age + '岁了!';
    alert(message);

ES6新增了一种模板字符串，表示方法和上面的多行字符串一样，但是它会自动替换字符串中的变量：

    var name = '小明';
    var age = 20;
    var message = `你好, ${name}, 你今年${age}岁了!`;
    alert(message);

### 操作字符串

1. `length`：字符串长度，指定字符可用s[i]，与Array操作相似，但是字符串是不可变的
2. `toUpperCase()、toLowerCase()`将字符串转换大小写
3. `indexOf()`会搜索指定字符串出现的位置
4. `substring()`返回指定索引区间的子串

---

<h2 id="2.4">数组</h2>

### 数组定义

JavaScript的Array可以包含任意数据类型，并通过索引来访问每个元素
要取得Array的长度，直接访问length属性：
**注意**:直接给Array的length赋一个新的值会导致Array大小的变化

### 操作数组

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

### `for`

JavaScript的循环有两种，一种是`for`循环，通过初始条件、结束条件和递增条件来循环执行语句块

`fo`r循环的3个条件都是可以省略的，如果没有退出循环的判断条件，就必须使用break语句退出循环，否则就是死循环

for循环的一个变体是`for ... in`循环，它可以把一个对象的所有属性依次循环出来:

    var o = {
        name: 'Jack',
        age: 20,
        city: 'Beijing'
    };
    for (var key in o) {
        alert(key); // 'name', 'age', 'city'
    }

*注*：for ... in对Array的循环得到的是String而不是Numbe

### `while`

while循环只有一个判断条件，条件满足，就不断循环，条件不满足时则退出循环。

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

<h2 id="3.3">方法</h1>

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

