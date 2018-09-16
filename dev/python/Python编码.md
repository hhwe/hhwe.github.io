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
