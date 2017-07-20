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

---

## Collections

### map / filter

和Array的`map()`与`filter(`)类似，但是underscore的`map()`和`filter()`可以作用于Object。当作用于Object时，传入的函数为`function (value, key)`，第一个参数接收value，第二个参数接收key

Object作`_.map()`操作的返回结果是Array,`_.mapObject()`返回对象

### every / some

当集合的所有元素都满足条件时，`_.every()`函数返回true，当集合的至少一个元素满足条件时，`_.some()`函数返回true

### max / min

`_max()`,`_min()`这两个函数直接返回集合中最大和最小的数,
集合是Object，`max()`和`min()`只作用于value，忽略掉key

### groupBy

`groupBy()`把集合的元素按照key归类，key由传入的函数返回,用来分组是非常方便的

### shuffle / sample

`shuffle()`用洗牌算法随机打乱一个集合,`sample()`则是随机选择一个或多个元素:

    _.sample([1, 2, 3, 4, 5, 6]); // 2
    _.sample([1, 2, 3, 4, 5, 6], 3); // 随机选3个：[6, 1, 4]


---

## Arrays

- `first()`/`last()`:顾名思义，这两个函数分别取第一个和最后一个元素
- `flatten()`接收一个Array，无论这个Array里面嵌套了多少个Array，最后都把它们变成一个一维数组
- `zip()`/`unzip()`把两个或多个数组的所有元素按索引对齐，然后按索引合并成新数组,`unzip()``与zip()`相反
- `object()`把两个或多个数组的所有元素按索引对齐，然后按索引合并成新对象
- `range()`让你快速生成一个序列，不再需要用`for`循环实现了

## Functions

- `bind()`可以帮我们把console对象直接绑定在log()的this指针上，以后调用log()就可以直接正常调用了
- `partial()`就是为一个函数创建偏函数
- `memoize()`对于相同的调用，第二次调用并没有计算，而是直接返回上次计算后缓存的结果
- `once()`保证某个函数执行且仅执行一次
- `delay()`可以让一个函数延迟执行，效果和`setTimeout()`是一样的，但是代码明显简单了

## Objects

- `keys()`可以非常方便地返回一个object自身所有的key，但不包含从原型链继承下来的，`allKeys()`除了object自身的key，还包含从原型链继承下来的
- `values()`返回object自身但不包含原型链继承的所有值，没有`allValues()`
- `mapObject()`就是针对object的map版本
- `invert()`把object的每个key-value来个交换，key变成value，value变成key
- `extend()`把多个object的key-value合并到第一个object并返回，`extendOwn()`和`extend()`类似，但获取属性时忽略从原型链继承下来的属性
- `clone()`会把原有对象的所有属性都复制到新的对象中
- `isEqual()`对两个object进行深度比较，如果内容完全相同，则返回true

**注**:
- 如果有相同的key，后面的object的value将覆盖前面的object的value
- clone()是“浅复制”。所谓“浅复制”就是说，两个对象相同的key所引用的value其实是同一对象

## Chaining

underscore提供了把对象包装成能进行链式调用的方法，就是`chain()`函数

因为每一步返回的都是包装对象，所以最后一步的结果需要调用`value()`获得最终结果