# python 日志

<!-- TOC -->

- [python 日志](#python-日志)
    - [Python是什么](#python是什么)
    - [Python中万物皆对象,对象有可变(mutable)与不可变(immutable)对象](#python中万物皆对象对象有可变mutable与不可变immutable对象)
    - [元类(metaclass)](#元类metaclass)
    - [@staticmethod,@classmethod,@property,@abstractmethod](#staticmethodclassmethodpropertyabstractmethod)
    - [生成器,迭代器](#生成器迭代器)
    - [Python垃圾回收GC和全局锁GIL](#python垃圾回收gc和全局锁gil)

<!-- /TOC -->

## Python是什么

1. python是一种解释性语言, 这就意味着他不会像C系语言一样需要运行前编译,写好代码就可以直接运行
2. python是一种动态语言,不需要再声明变量前考虑类型,变量类型在运行中可以改变
3. python是面向对象的语言,支持继承,封装,多态,但是python没有完全的私有变量,所有变量都是可以使用的,python中万物皆对象
4. python开发效率高,但是运行效率低,可以在python中使用C来运行计算密集型任务
5. python是一种高级语言,所以程序员可以专注于写算法和结构,而不是细节的低级细节

## Python中万物皆对象,对象有可变(mutable)与不可变(immutable)对象

在python中,strings,tuples,和numbers是不可变的对象,而 list,dict,set 等则是可变的对象可变对象在修改的时候只修改对象本身,不可变对象在修改时候会重新新建一个新的对象,将修改后的值传递给它

当一个引用传递给函数的时候,函数自动复制一份引用,这个函数里的引用和外边的引用没有半毛关系了而在参数传递的时候变量都是通过传递对象的引用(指针),如果在域内修改不可变对象,将会创建新的对象,Python中没有块变量域

```python
def f(x,l=[]):
    for i in range(x):
        l.append(i*i)
    print(l)

f(2)  # [0, 1]
f(3,[3,2,1])  # [3, 2, 1, 0, 1, 4]
f(3)  # [0, 1, 0, 1, 4]
```

## 元类(metaclass)

`type()`函数既可以返回一个对象的类型,又可以创建出新的类型

```python
class Hello(object):
    def hello(self,name='world'):
        print('Hello,%s.' % name)


type(Hello)  # <class 'type'>
type('Hello',(object,),dict(hello=fn))  # 动态创建类
```

除了使用`type()`动态创建类以外,要控制类的创建行为,还可以使用`metaclass`,metaclass的类名总是以`Metaclass`结尾,以便清楚地表示这是一个metaclass:

```python
# metaclass是类的模板,所以必须从`type`类型派生：
class ListMetaclass(type):
    def __new__(cls, name, bases, attrs):
        attrs['add'] = lambda self, value: self.append(value)
        return type.__new__(cls, name, bases, attrs)


# 定义类的时候还要指示使用ListMetaclass来定制类,传入关键字参数metaclass
class MyList(list, metaclass=ListMetaclass):
    pass
```

## @staticmethod,@classmethod,@property,@abstractmethod

```python
def foo(x):
    print(f"{x}")


class A(object):
    # __slots__定义的属性仅对当前类起作用,对继承的子类是不起作用的
    # 除非在子类中也定义__slots__,这样,子类允许定义的属性就是自身的__slots__加上父类的__slots__
    __slots__ = ('name', 'var_of_instance', '_age')  # 限制实例属性
    var_of_class = 1  # 类属性

    def __init__(self, name):
        self.name = name
        self.var_of_instance = 0
        self._age = 0

    def foo(self, x):
        print(f"{self} -> {x}")

    @classmethod
    def class_foo(cls, x):
        print(f"{cls} ->{x}")

    @staticmethod
    def static_foo(x):
        print(f"{x}")

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, age):
        self._age = age


foo(10)
a = A("han")
print(f"{a} -> {a.var_of_class} -> {a.var_of_instance}")
print(f"{a.__class__} -> {A.var_of_class} -> {a.__class__.var_of_class}")

# 实例方法需要绑定对应的实例,可通过实例调用,或者函数中传入实例
a.foo(123)  # 123
# A.foo(123)  # TypeError: foo() missing 1 required positional argument: 'x'
A.foo(a, 456)  # 456
A.foo(A, 789)  # 789
# 类方法是绑定到类的
A.class_foo(123)  # 123
a.class_foo(456)  # 456
# 静态方法就和普通方法一样,只不过是放在类中,方便使用
A.static_foo(456)  # 123
a.static_foo(456)  # 456

# 可以给类动态添加属性,但是无法对实例添加slots之外属性,会报错
A.pk = 10
print(A.pk)  # 10
# a.bk = 10  # AttributeError: 'A' object has no attribute 'bk'

# 通过@property可以为实例添加属性
print(a.age)
a.age = 10
print(a.age)


# python中抽象函数
from abc import ABC, abstractmethod


class A(ABC):
    @abstractmethod
    def abstract_method(self):
        """ 在子类中实现该方法,才可以实例化 """


class SubA(A):
    def abstract_method(self):
        print("必须实现abstract method才可以实例化")


# a = A()  # TypeError: Can't instantiate abstract class A with abstract methods abstract_method
b = SubA()
```

## 生成器,迭代器

```python
# Iterable 可迭代对象,可以使用for...in...都是可迭代对象
li = [x*x for x in range(10)]  # 列表生成器一次性将所有元素读入到内存中
# Generators 迭代器,每次只能迭代一次,不会将所有值存储在内存中,它们会动态生成值
ge = (x*x for x in range(10))  # 由于生成器只能使用一次,读完就会删掉
def gn():
    for i in range(3):
        n = yield i*i  # 使用yield生成器
        print(n)
g = gn()  # 调用的时候不会执行函数体,而是返回生成器对象
for i in g:  # 用for可以执行函数,但是每次执行回到yield返回
    print(i)
print("============")
g = gn()
print(next(g))  # 生成器可以使用next()函数执行
print(g.__next__())
print(next(g))
# print(next(g))  # StopIteration 最后一个迭代完在使用会报错
print("============")
g = gn()
print(g.send(None))  # 生成器也可以使用send()迭代,第一次参数必须是None
print(g.send(1))  # next(g)相当于g.send(None)
print(g.send(2))
# print(g.send(3))  # StopIteration 最后一个迭代完在使用会报错
```

## Python垃圾回收GC和全局锁GIL

* 引用计数,当对象有新的引用就加一,删掉一个引用就减一,但是无法解决循环引用
* 标记清除,遍历所有对象,可访问对象打上标记,释放掉没有标记的对象
* 分代回收,存活时间越久垃圾收集频率越小,索引数越大,对象存活时间越长

```python
import sys
l = []
a = l
r = []
b = r
r.append(l)
l.append(r)
print(sys.getrefcount(a))  # 4
print(sys.getrefcount(b))  # 4
del l
del r
print(sys.getrefcount(a))  # 3
print(sys.getrefcount(b))  # 3
```

> Python的解释器必须做到既安全又高效. 我们都知道多线程编程会遇到的问题. 解释器要留意的是避免在不同的线程操作内部共享的数据. 同时它还要保证在管理用户线程时保证总是有最大化的计算资源.
> 那么,不同线程同时访问时,数据的保护机制是怎样的呢？答案是解释器全局锁. 从名字上看能告诉我们很多东西,很显然,这是一个加在解释器上的全局(从解释器的角度看)锁(从互斥或者类似角度看).
> CPython的线程是操作系统的原生线程. 在Linux上为pthread,在Windows上为Win thread,完全由操作系统调度线程的执行. 一个Python解释器进程内有一个主线程,以及多个用户程序的执行线程. 即便使用多核心CPU平台,由于GIL的存在,也将禁止多线程的并行执行.
> Python解释器进程内的多线程是以协作多任务方式执行. 当一个线程遇到I/O任务时,将释放GIL. 计算密集型(CPU-bound)的线程在执行大约100次解释器的计步(ticks)时,将释放GIL. 计步(ticks)可粗略看作Python虚拟机的指令. 计步实际上与时间片长度无关. 可以通过sys.setcheckinterval()设置计步长度.
> 在单核CPU上,数百次的间隔检查才会导致一次线程切换. 在多核CPU上,存在严重的线程颠簸(thrashing).
> Python 3.2开始使用新的GIL. 新的GIL实现中用一个固定的超时时间来指示当前的线程放弃全局锁. 在当前线程保持这个锁,且其他线程请求这个锁时,当前线程就会在5毫秒后被强制释放该锁.
> 可以创建独立的进程来实现并行化. Python 2.6引进了多进程包multiprocessing. 或者将关键组件用C/C++编写为Python扩展,通过ctypes使Python程序直接调用C语言编译的动态链接库的导出函数.
