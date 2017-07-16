---
title: 2017-07-15-JavaScript-Tutorial
date: 2017-07-15 08:29:32
categories: JS
tags: 
    - JS
    - tutorial
---

# 目录

*   [标准对象](#4.0)  
    *   [Date](#4.1)
    *   [RegExp](#4.2)
    *   [JSON](#4.3)
*   [面向对象编程](#5.0)
    *   [创建对象](#5.1)
    *   [原型继承](#5.2)
    *   [class继承](#5.3)


---


<h1 id="4.0">标准对象</h1>

在JavaScript的世界里，一切都是对象。

但是某些对象还是和其他对象不太一样。为了区分对象的类型，我们用`typeof`操作符获取对象的类型，它总是返回一个字符串：

    typeof 123; // 'number'
    typeof NaN; // 'number'
    typeof 'str'; // 'string'
    typeof true; // 'boolean'
    typeof undefined; // 'undefined'
    typeof Math.abs; // 'function'
    typeof null; // 'object'
    typeof []; // 'object'
    typeof {}; // 'object'

### 包装对象

number、boolean和string都有包装对象。没错，在JavaScript中，字符串也区分string类型和它的包装类型。包装对象用new创建：

    var n = new Number(123); // 123,生成了新的包装类型
    typeof new Number(123); // 'object'
    var b = new Boolean(true); // true,生成了新的包装类型
    var s = new String('str'); // 'str',生成了新的包装类型

总结一下，有这么几条规则需要遵守：

- 不要使用new Number()、new Boolean()、new String()创建包装对象；
- 用parseInt()或parseFloat()来转换任意类型到number；
- 用String()来转换任意类型到string，或者直接调用某个对象的toString()方法；
- 通常不必把任意类型转换为boolean再判断，因为可以直接写if (myVar) {...}；
- typeof操作符可以判断出number、boolean、string、function和undefined；
- 判断Array要使用Array.isArray(arr)；
- 判断null请使用myVar === null；
- 判断某个全局变量是否存在用typeof window.myVar === 'undefined'；
- 函数内部判断某个变量是否存在用typeof myVar === 'undefined'。

*注*：number对象调用toString()报SyntaxError

---

<h2 id="4.1">Date</h2>

在JavaScript中，Date对象用来表示日期和时间。

    var now = new Date();
    now; // Wed Jun 24 2015 19:49:22 GMT+0800 (CST)
    now.getFullYear(); // 2015, 年份
    now.getMonth(); // 5, 月份，注意月份范围是0~11，5表示六月
    now.getDate(); // 24, 表示24号
    now.getDay(); // 3, 表示星期三
    now.getHours(); // 19, 24小时制
    now.getMinutes(); // 49, 分钟
    now.getSeconds(); // 22, 秒
    now.getMilliseconds(); // 875, 毫秒数
    now.getTime(); // 1435146562875, 以number形式表示的时间戳

---

<h2 id="4.2">RegExp</h2>

在正则表达式中，如果直接给出字符，就是精确匹配

- `\d`        可以匹配一个数字
- `\w`        可以匹配一个字母或数字
- `.`         可以匹配任意字符
- `*`         表示任意个字符（包括0个）
- `+`         表示至少一个字符
- `?`         表示0个或1个字符
- `{n}`       表示n个字符
- `{n,m}`     表示n-m个字符
- `\s`        可以匹配一个空格
- `[]`        表示范围
- `A|B`       可以匹配A或B
- `^`         表示行的开头
- `$`         表示行的结束 
                 
JavaScript有两种方式创建一个正则表达式：

第一种方式是直接通过`/正则表达式/`写出来，第二种方式是通过`new RegExp('正则表达式')`创建一个RegExp对象。

两种写法是一样的：

    var re1 = /ABC\-001/;
    var re2 = new RegExp('ABC\\-001');
    re1; // /ABC\-001/
    re2; // /ABC\-001/

RegExp对象的`test()`方法用于测试给定的字符串是否符合条件

    re1.test('ABC\-001') //true

`split()`正则表达式切分字符串比用固定的字符更灵活

    'a,b;; c  d'.split(/[\s\,\;]+/); // ['a', 'b', 'c', 'd']

用`()`表示的就是要提取的分组（Group）。比如：`^(\d{3})-(\d{3,8})$`分别定义了两个组，可以直接从匹配的字符串中提取出区号和本地号码：

正则表达式中定义了组，就可以在RegExp对象上用`exec()`方法提取出子串来

    var re = /^(\d{3})-(\d{3,8})$/;
    re.exec('010-12345'); // ['010-12345', '010', '12345']
    re.exec('010 12345'); // null

`exec()`方法在匹配成功后，会返回一个Array，第一个元素是正则表达式匹配到的整个字符串，后面的字符串表示匹配成功的子串。

### 贪婪匹配

正则匹配默认是贪婪匹配，也就是匹配尽可能多的字符

    var re = /^(\d+)(0*)$/;
    re.exec('102300'); // ['102300', '102300', '']

由于`\d+`采用贪婪匹配，直接把后面的0全部匹配了，结果`0*`只能匹配空字符串了。

必须让`\d+`采用非贪婪匹配（也就是尽可能少匹配），才能把后面的`0`匹配出来，加个`?`就可以让`\d+`采用非贪婪匹配：

    var re = /^(\d+?)(0*)$/;
    re.exec('102300'); // ['102300', '1023', '00']

### 全局搜索

JavaScript的正则表达式还有几个特殊的标志，最常用的是`g`，表示全局匹配

全局匹配可以多次执行`exec()`方法来搜索一个匹配的字符串。当我们指定`g`标志后，每次运行`exec()`，正则表达式本身会更新`lastIndex`属性，表示上次匹配到的最后索引

全局匹配类似搜索，因此不能使用`/^...$/`，那样只会最多匹配一次。

正则表达式还可以指定`i`标志，表示忽略大小写，`m`标志，表示执行多行匹配

---

<h2 id="4.3">JSON</h2>

JSON是JavaScript Object Notation的缩写，它是一种数据交换格式

**JSON 是 JS 对象的字符串表示法，它使用文本表示一个 JS 对象的信息，本质是一个字符串**

JSON 数据的书写格式是：名称/值对。名称/值对包括字段名称（在双引号中），后面写一个冒号，然后是值

要实现从对象转换为 JSON 字符串，使用 `JSON.stringify()` 方法：

    var json = JSON.stringify({a: 'Hello', b: 'World'}); //结果是 '{"a": "Hello", "b": "World"}'

要实现从 JSON 转换为对象，使用 `JSON.parse()` 方法：

    var obj = JSON.parse('{"a": "Hello", "b": "World"}'); //结果是 {a: 'Hello', b: 'World'}

JSON 最常见的用法之一，是从 web 服务器上读取 JSON 数据（作为文件或作为 HttpRequest），将 JSON 数据转换为 JavaScript 对象，然后在网页中使用该数据。

JavaScript 函数 eval() 可用于将 JSON 文本转换为 JavaScript 对象

---

<h1 id="5.0">面向对象编程</h1>

JavaScript不区分类和实例的概念，而是通过原型（prototype）来实现面向对象编程。avaScript的原型链和Java的Class区别就在，它没有“Class”的概念，所有对象都是实例，所谓继承关系不过是把一个对象的原型指向另一个对象而已

直接用`obj.__proto__`去改变一个对象的原型，

    var Student = {
        name: 'Robot'
    };
    var xiaoming = {
        name: '小明'
    };
    xiaoming.__proto__ = Student;

不要直接用`obj.__proto__`去改变一个对象的原型，`Object.create()`方法可以传入一个原型对象，并创建一个基于该原型的新对象

    var Student = {     // 原型对象
        name: 'Robot',
        height: 1.2,
        run: function () {
            console.log(this.name + ' is running...');
        }
    };
    function createStudent(name) {
        var s = Object.create(Student); // 基于Student原型创建一个新对象:
        s.name = name;// 初始化新对象:
        return s;
    }
    var xiaoming = createStudent('小明');
    xiaoming.run(); // 小明 is running...
    xiaoming.__proto__ === Student; // true

---

<h2 id="5.1">创建对象</h2>

JavaScript 基于 `prototype`，而不是基于类的，JavaScript对每个创建的对象都会设置一个原型，指向它的原型对象。

当我们用obj.xxx访问一个对象的属性时，JavaScript引擎先在当前对象上查找该属性，如果没有找到，就到其原型对象上找，如果还没有找到，就一直上溯到Object.prototype对象，最后，如果还没有找到，就只能返回undefined。

例如，创建一个Array对象，其原型链是：arr ----> Array.prototype ----> Object.prototype ----> null

创建新对象有两种不同的方法：
-   定义并创建对象的实例
-   使用函数来定义对象，然后创建新的对象实例

除了直接用`{ ... }`创建一个对象外，JavaScript还可以用一种构造函数的方法来创建对象。它的用法是，先定义一个构造函数，再用关键字`new`来调用这个函数，并返回一个对象

    function Student(name) {
        this.name = name;
        this.hello = function () {
            alert('Hello, ' + this.name + '!');
        }
    }
    var xiaoming = new Student('小明');
    xiaoming.name; // '小明'
    xiaoming.hello(); // Hello, 小明!

用`new Student()`创建的对象还从原型上获得了一个`constructor`属性，它指向函数Student本身

新创建的xiaoming的原型链是：

![](/images/2017-07-15-1.png)

共享同一个函数可以将函数绑定到函数原型上，如`Student.prototype`:

    function Student(name) {
        this.name = name;
    }

    Student.prototype.hello = function () {
        alert('Hello, ' + this.name + '!');
    };

![](/images/2017-07-15-2.png)

---

<h2 id="5.2">原型继承</h2>

我们必须借助一个中间对象来实现正确的原型链，这个中间对象的原型要指向`Student.prototype`。为了实现这一点，参考道爷（就是发明JSON的那个道格拉斯）的代码，中间对象可以用一个空函数F来实现：

    // PrimaryStudent构造函数:
    function PrimaryStudent(props) {
        Student.call(this, props);
        this.grade = props.grade || 1;
    }
    // 空函数F:
    function F() {
    }
    // 把F的原型指向Student.prototype:
    F.prototype = Student.prototype;
    // 把PrimaryStudent的原型指向一个新的F对象，F对象的原型正好指向Student.prototype:
    PrimaryStudent.prototype = new F();
    // 把PrimaryStudent原型的构造函数修复为PrimaryStudent:
    PrimaryStudent.prototype.constructor = PrimaryStudent;
    // 继续在PrimaryStudent原型（就是new F()对象）上定义方法：
    PrimaryStudent.prototype.getGrade = function () {
        return this.grade;
    };
    // 创建xiaoming:
    var xiaoming = new PrimaryStudent({
        name: '小明',
        grade: 2
    });
    xiaoming.name; // '小明'
    xiaoming.grade; // 2
    // 验证原型:
    xiaoming.__proto__ === PrimaryStudent.prototype; // true
    xiaoming.__proto__.__proto__ === Student.prototype; // true

    // 验证继承关系:
    xiaoming instanceof PrimaryStudent; // true
    xiaoming instanceof Student; // true

原型链图：

![](/images/2017-07-15-3.png)

如果把继承这个动作用一个`inherits()`函数封装起来，还可以隐藏`F`的定义，并简化代码：

    function inherits(Child, Parent) {
        var F = function () {};
        F.prototype = Parent.prototype;
        Child.prototype = new F();
        Child.prototype.constructor = Child;
    }

JavaScript的原型继承实现方式就是：

- 定义新的构造函数，并在内部用`call()`调用希望“继承”的构造函数，并绑定`this`；
- 借助中间函数`F`实现原型链继承，最好通过封装的`inherits`函数完成；
- 继续在新的构造函数的原型上定义新方法。


---

<h2 id="5.3">class继承</h2>

新的关键字`class`从ES6开始正式被引入到JavaScript中。`class`的目的就是让定义类更简单。

用函数实现Student的方法：

    function Student(name) {
        this.name = name;
    }
    Student.prototype.hello = function () {
        alert('Hello, ' + this.name + '!');
    }

用新的class关键字来编写Student，可以这样写：

    class Student {
        constructor(name) {
            this.name = name;
        }
        hello() {
            alert('Hello, ' + this.name + '!');
        }
    }

原型继承的中间对象，原型对象的构造函数等等都不需要考虑了，直接通过`extends`来实现：

    class PrimaryStudent extends Student {
        constructor(name, grade) {
            super(name); // 记得用super调用父类的构造方法!
            this.grade = grade;
        }
        myGrade() {
            alert('I am at grade ' + this.grade);
        }
    }

