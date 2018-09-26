## 编码

使用python开发有一年了, 目前公司项目还是比较老的python2开发, 过程中遇到的最大的问题是**编码**, 这个说实话一开始是真的不了解, 特别是在不同的开发环境中会出现很大的差异, 对于一个小白来首简直是灾难. 我也一直将编码问题收集起来做分析, 也看了很多网上对python编码的文章, 颇有心得, 总结一下.

## 编码是什么??

判断编码
``` python
    @property
    def apparent_encoding(self):
        """The apparent encoding, provided by the chardet library."""
        return chardet.detect(self.content)['encoding']
```

字节到字符串
``` python
str(object='') -> str
str(bytes_or_buffer[, encoding[, errors]]) -> str
Create a new string object from the given object. If encoding or
errors is specified, then the object must expose a data buffer
that will be decoded using the given encoding and error handler.
Otherwise, returns the result of object.__str__() (if defined)
or repr(object).
encoding defaults to sys.getdefaultencoding().
errors defaults to 'strict'.
```

## 进制装换

进制间的转换可以用int(str, base=10)转换成十进制, 在转换成其他进制

```python
# 其他进制字符转十进制
int(x, base=10)
# 十进制转二进制
bin(10)  # '0b1010'
# 十进制转八进制
oct(10)  # '0o12'
# 十进制转十六进制
hex(10)  # '0xa'
# 字符装换成数字
ord('A')  # 65
# 数字转换成字符
chr(65)  # 'A'
```

## 切片

如果用到切片的sep, 是每次指针移动的位数, -1 表示网后移动以为, 1往前移动

```python
i = 'a'
bin(int(i, base=16))[3::-1]
Out[3]: '01b0'
bin(int(i, base=16))
Out[4]: '0b1010'
bin(int(i, base=16))[2::-1]
Out[5]: '1b0'
bin(int(i, base=16))[2::][::-1]
Out[6]: '0101'
```

## 格式化字符串

```python
# 1. 使用`%`号
print("%s's age %d" % ("han", 25))  # han's age 25
# 2. 使用format函数
print("{}'s age {}".format("han", 25))  # han's age 25
# 3. 使用f表达式
name = "han"
age = 25
print(f"{name}'s age {age}")  # han's age 25
# 4. 使用string自带的template模板
from string import Template
Template("$name's age is $age").substitute(name='han', age=25)  # han's age 25
```
