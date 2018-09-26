# Pandas快速入门教程

<!-- TOC -->

- [Pandas快速入门教程](#pandas快速入门教程)
    - [概述](#概述)
        - [数据结构](#数据结构)
        - [为什么有多个数据结构](#为什么有多个数据结构)
        - [可变性和数据复制](#可变性和数据复制)
    - [Pandas简单入门](#pandas简单入门)
        - [对象创建](#对象创建)
        - [查看数据](#查看数据)
        - [Selection](#selection)
            - [Getting](#getting)
            - [按标签选择](#按标签选择)
            - [按位置选择](#按位置选择)
            - [布尔索引](#布尔索引)
            - [设定](#设定)
        - [缺少数据](#缺少数据)
        - [操作](#操作)
            - [统计](#统计)
            - [apply](#apply)
            - [直方图](#直方图)
            - [字符串方法](#字符串方法)
        - [Merge](#merge)
            - [Concat](#concat)
            - [加入](#加入)
            - [追加](#追加)
        - [分组](#分组)
        - [Reshaping](#reshaping)
            - [堆栈](#堆栈)
            - [数据透视表](#数据透视表)
        - [时间序列](#时间序列)
        - [分类](#分类)
        - [绘图](#绘图)
        - [获取数据进/出](#获取数据进出)
            - [CSV](#csv)
            - [HDF5](#hdf5)
            - [Excel中](#excel中)
        - [陷阱](#陷阱)

<!-- /TOC -->

## 概述

**pandas**是一个[Python](http://www.python.org/)包, 提供快速, 灵活和富有表现力的数据结构, 旨在使“关系”或“标记”数据的使用既简单又直观. 它旨在成为在Python中进行实际, **真实世界**数据分析的基础高级构建块. 此外, 它还有更广泛的目标, 即成为**任何语言中最强大, 最灵活的开源数据分析/操作工具**. 它已朝着这个目标迈进. 

Pandas非常适合许多不同类型的数据：

* 具有异构类型列的表格数据, 如SQL表或Excel电子表格中
* 有序和无序(不一定是固定频率)时间序列数据. 
* 具有行和列标签的任意矩阵数据(均匀类型或异构)
* 任何其他形式的观察/统计数据集. 实际上不需要将数据标记为放置在pandas数据结构中

Pandas的两个主要数据结构[`Series`](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.html#pandas.Series "pandas.Series")(1维)和[`DataFrame`](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html#pandas.DataFrame "pandas.DataFrame")(2维)处理金融, 统计, 社会科学和许多工程领域中的绝大多数典型用例. 对于R用户, [`DataFrame`](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html#pandas.DataFrame "pandas.DataFrame")提供R 提供的所有内容 `data.frame`以及更多内容. pandas建立在[NumPy之上](http://www.numpy.org/), 旨在与许多其他第三方库完美地集成在科学计算环境中. 

以下是Pandas做得很好的一些事情：

* 轻松处理浮点中的**缺失数据**(表示为NaN)以及非浮点数据
* 大小可变性：可以从DataFrame和更高维对象**插入和删除**列
* 自动和显式**数据对齐**：对象可以显式对齐到一组标签, 或者用户可以简单地忽略标签, 让<cite>Series</cite>, <cite>DataFrame</cite>等在计算中自动对齐数据
* 功能强大, 灵活的**分组**功能, 可对数据集执行拆分应用组合操作, 以便聚合和转换数据
* 可以**轻松地将**其他Python和NumPy数据结构中的不规则索引数据**转换**为DataFrame对象
* 基于智能标签的**切片**, **花式索引**和 大型数据集的**子**集化
* 直观的**合并**和**连接**数据集
* 灵活的数据集**整形**和旋转
* 轴的**分层**标记(每个刻度可能有多个标签)
* 强大的IO工具, 用于从**平面文件**(CSV和分隔), Excel文件, 数据库加载数据, 以及从超快速**HDF5格式**保存/加载数据
* **时间序列** - 特定功能：日期范围生成和频率转换, 移动窗口统计, 移动窗口线性回归, 日期转换和滞后等. 

其中许多原则旨在解决使用其他语言/科学研究环境时经常遇到的缺点. 对于数据科学家来说, 处理数据通常分为多个阶段：整理和清理数据, 分析/建模数据, 然后将分析结果组织成适合绘图或表格显示的形式. Pandas是完成所有这些任务的理想工具. 

其他一些说明

* Pandas**很快**. 许多低级算法位已经在[Cython](http://cython.org/)代码中进行了大量调整. 然而, 与其他任何事物一样, 通常会牺牲性能. 因此, 如果您专注于应用程序的一个功能, 您可以创建一个更快的专用工具. 
* pandas是[statsmodels](http://www.statsmodels.org/stable/index.html)的依赖, 使其成为Python中统计计算生态系统的重要组成部分. 
* Pandas已广泛用于金融应用的生产中. 

注意

本文档假定您对NumPy有一般的了解. 如果您还没有多少使用[过NumPy, ](http://docs.scipy.org/)请先投入一些时间来[学习NumPy](http://docs.scipy.org/). 

### 数据结构

[`pandas`](http://pandas.pydata.org/pandas-docs/stable/index.html#module-pandas "Pandas") 由以下元素组成：

* 一组带标签的数组数据结构, 主要是Series和DataFrame. 
* 索引对象启用简单轴索引和多级/分层轴索引. 
* 引擎的集成组, 用于聚合和转换数据集. 
* 日期范围生成(date_range)和自定义日期偏移, 可实现自定义频率. 
* 输入/输出工具：从平面文件(CSV, 分隔符, Excel 2003)加载表格数据, 以及从快速有效的PyTables / HDF5格式保存和加载pandas对象. 
* 内存高效的“稀疏”版本的标准数据结构, 用于存储大部分缺失或大部分不变的数据(某些固定值). 
* 移动窗口统计(滚动平均值, 滚动标准偏差等)

| Dimensions | Name      | Description                                                                                      |
| ---------- | --------- | ------------------------------------------------------------------------------------------------ |
| 1          | Series    | 1D labeled homogeneously-typed array                                                             |
| 2          | DataFrame | General 2D labeled, size-mutable tabular structure with potentially heterogeneously-typed column |

### 为什么有多个数据结构

考虑pandas数据结构的最佳方式是作为低维数据的灵活容器. 例如, DataFrame是Series的容器, Series是scalars的容器. 我们希望能够以类似字典的方式插入和删除这些容器中的对象. 

此外, 我们希望通用API函数的合理默认行为考虑到时间序列和横截面数据集的典型方向. 当使用ndarrays存储2维和3维数据时, 在编写函数时会给用户带来负担以考虑数据集的方向; 轴被认为或多或少相等(除非C-或Fortran-连续性对性能有影响). 在Pandas中, 轴旨在为数据提供更多的语义含义; 即, 对于特定数据集, 可能存在定向数据的“正确”方式. 因此, 目标是减少在下游功能中编码数据转换所需的心理努力量. 

例如, 对于表格数据(DataFrame), 考虑**索引**(行)和**列**而不是轴0和轴1 在语义上更有帮助. 迭代DataFrame的列因此导致更易读的代码：

```python
for col in df.columns:
    series = df[col]
    # do something with series
```

### 可变性和数据复制

所有pandas数据结构都是值可变的(它们包含的值可以改变)但不总是大小可变的. 无法更改Series的长度, 但是, 例如, 可以将列插入到DataFrame中. 但是, 绝大多数方法都会生成新对象并保持输入数据不变. 一般来说, 我们喜欢在合情合理的情况下**支持不变性**. 

## Pandas简单入门

这是对Pandas的简短介绍, 主要面向新用户. 您可以在[Cookbook](http://pandas.pydata.org/pandas-docs/stable/cookbook.html#cookbook)看到更复杂的应用. 

通常, 我们导入如下：

```python
In [1]: import pandas as pd
In [2]: import numpy as np
In [3]: import matplotlib.pyplot as plt
```

### 对象创建

请参阅[数据结构简介部分](http://pandas.pydata.org/pandas-docs/stable/dsintro.html#dsintro). 

通过传递值的列表来创建一个[`Series`](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.html#pandas.Series "pandas.Series"), 让Pandas创建一个默认的整数索引：

```python
In [4]: s = pd.Series([1,3,5,np.nan,6,8])
In [5]: s
Out[5]: 
0    1.0
1    3.0
2    5.0
3    NaN
4    6.0
5    8.0
dtype: float64
```

[`DataFrame`](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html#pandas.DataFrame "pandas.DataFrame")通过传递带有日期时间索引和标记列的NumPy数组来创建：

```python
In [6]: dates = pd.date_range('20130101', periods=6)
In [7]: dates
Out[7]: 
DatetimeIndex(['2013-01-01', '2013-01-02', '2013-01-03', '2013-01-04',
 '2013-01-05', '2013-01-06'],
 dtype='datetime64[ns]', freq='D')
In [8]: df = pd.DataFrame(np.random.randn(6,4), index=dates, columns=list('ABCD'))
In [9]: df
Out[9]: 
                   A         B         C         D
2013-01-01  0.469112 -0.282863 -1.509059 -1.135632
2013-01-02  1.212112 -0.173215  0.119209 -1.044236
2013-01-03 -0.861849 -2.104569 -0.494929  1.071804
2013-01-04  0.721555 -0.706771 -1.039575  0.271860
2013-01-05 -0.424972  0.567020  0.276232 -1.087401
2013-01-06 -0.673690  0.113648 -1.478427  0.524988
```

`DataFrame`通过传递可以转换为类似系列的对象的dict来创建. 

```python
In [10]: df2 = pd.DataFrame({ 'A' : 1.,
 ....:                     'B' : pd.Timestamp('20130102'),
 ....:                     'C' : pd.Series(1,index=list(range(4)),dtype='float32'),
 ....:                     'D' : np.array([3] * 4,dtype='int32'),
 ....:                     'E' : pd.Categorical(["test","train","test","train"]),
 ....:                     'F' : 'foo' })
 ....: 

In [11]: df2
Out[11]: 
     A          B    C  D      E    F
0  1.0 2013-01-02  1.0  3   test  foo
1  1.0 2013-01-02  1.0  3  train  foo
2  1.0 2013-01-02  1.0  3   test  foo
3  1.0 2013-01-02  1.0  3  train  foo
```

结果的列`DataFrame`具有不同的 [dtypes](http://pandas.pydata.org/pandas-docs/stable/basics.html#basics-dtypes). 

```python
In [12]: df2.dtypes
Out[12]: 
A           float64
B    datetime64[ns]
C           float32
D             int32
E          category
F            object
dtype: object
```

如果您正在使用IPython, 则会自动启用列名称(以及公共属性)的选项卡完成. 以下是将要完成的属性的子集：

```python
In [13]: df2.<TAB>
df2.A                  df2.bool
df2.abs                df2.boxplot
df2.add                df2.C
df2.add_prefix         df2.clip
df2.add_suffix         df2.clip_lower
df2.align              df2.clip_upper
df2.all                df2.columns
df2.any                df2.combine
df2.append             df2.combine_first
df2.apply              df2.compound
df2.applymap           df2.consolidate
df2.D
```

正如你所看到的, 列`A`, `B`, `C`, 和`D`自动标签完成. `E`也有; 为简洁起见, 其他属性已被截断. 

### 查看数据

请参阅[`基础知识部分`](http://pandas.pydata.org/pandas-docs/stable/basics.html#basics). 

以下是查看frame的顶行和底行的方法：

```python
In [14]: df.head()
Out[14]: 
         A         B         C         D
2013-01-01  0.469112 -0.282863 -1.509059 -1.135632
2013-01-02  1.212112 -0.173215  0.119209 -1.044236
2013-01-03 -0.861849 -2.104569 -0.494929  1.071804
2013-01-04  0.721555 -0.706771 -1.039575  0.271860
2013-01-05 -0.424972  0.567020  0.276232 -1.087401

In [15]: df.tail(3)
Out[15]: 
         A         B         C         D
2013-01-04  0.721555 -0.706771 -1.039575  0.271860
2013-01-05 -0.424972  0.567020  0.276232 -1.087401
2013-01-06 -0.673690  0.113648 -1.478427  0.524988
```

显示索引, 列和基础NumPy数据：

```python
In [16]: df.index
Out[16]: 
DatetimeIndex(['2013-01-01', '2013-01-02', '2013-01-03', '2013-01-04',
               '2013-01-05', '2013-01-06'],
               dtype='datetime64[ns]', freq='D')
In [17]: df.columns
Out[17]: Index(['A', 'B', 'C', 'D'], dtype='object')

In [18]: df.values
Out[18]: 
array([[ 0.4691, -0.2829, -1.5091, -1.1356],
       [ 1.2121, -0.1732,  0.1192, -1.0442],
       [-0.8618, -2.1046, -0.4949,  1.0718],
       [ 0.7216, -0.7068, -1.0396,  0.2719],
       [-0.425 ,  0.567 ,  0.2762, -1.0874],
       [-0.6737,  0.1136, -1.4784,  0.525 ]])
```

[`describe()`](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.describe.html#pandas.DataFrame.describe "pandas.DataFrame.describe") 显示您的数据的快速统计摘要：

```python
In [19]: df.describe()
Out[19]: 
              A         B         C         D
count  6.000000  6.000000  6.000000  6.000000
mean   0.073711 -0.431125 -0.687758 -0.233103
std    0.843157  0.922818  0.779887  0.973118
min   -0.861849 -2.104569 -1.509059 -1.135632
25%   -0.611510 -0.600794 -1.368714 -1.076610
50%    0.022070 -0.228039 -0.767252 -0.386188
75%    0.658444  0.041933 -0.034326  0.461706
max    1.212112  0.567020  0.276232  1.071804
```

转置您的数据：

```python
In [20]: df.T
Out[20]: 
   2013-01-01  2013-01-02  2013-01-03  2013-01-04  2013-01-05  2013-01-06
A    0.469112    1.212112   -0.861849    0.721555   -0.424972   -0.673690
B   -0.282863   -0.173215   -2.104569   -0.706771    0.567020    0.113648
C   -1.509059    0.119209   -0.494929   -1.039575    0.276232   -1.478427
D   -1.135632   -1.044236    1.071804    0.271860   -1.087401    0.524988
```

按轴排序：

```python
In [21]: df.sort_index(axis=1, ascending=False)
Out[21]: 
                   D         C         B         A
2013-01-01 -1.135632 -1.509059 -0.282863  0.469112
2013-01-02 -1.044236  0.119209 -0.173215  1.212112
2013-01-03  1.071804 -0.494929 -2.104569 -0.861849
2013-01-04  0.271860 -1.039575 -0.706771  0.721555
2013-01-05 -1.087401  0.276232  0.567020 -0.424972
2013-01-06  0.524988 -1.478427  0.113648 -0.673690
```

按值排序：

```python
In [22]: df.sort_values(by='B')
Out[22]: 
                   A         B         C         D
2013-01-03 -0.861849 -2.104569 -0.494929  1.071804
2013-01-04  0.721555 -0.706771 -1.039575  0.271860
2013-01-01  0.469112 -0.282863 -1.509059 -1.135632
2013-01-02  1.212112 -0.173215  0.119209 -1.044236
2013-01-06 -0.673690  0.113648 -1.478427  0.524988
2013-01-05 -0.424972  0.567020  0.276232 -1.087401
```

### Selection

**注意:** 虽然标准的Python/Numpy的选择和设置表达式直观并且方便互动工作, 在实际的代码中我们建议优化的Pandas数据访问方法：`.at`, `.iat`, `.loc`和`.iloc`. 

请参阅索引文档[索引和选择数据](http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing)以及[MultiIndex / Advanced索引](http://pandas.pydata.org/pandas-docs/stable/advanced.html#advanced). 

#### Getting

选择一个列, 产生一个`Series`, 相当于`df.A`：

```python
In [23]: df['A']
Out[23]: 
2013-01-01    0.469112
2013-01-02    1.212112
2013-01-03   -0.861849
2013-01-04    0.721555
2013-01-05   -0.424972
2013-01-06   -0.673690
Freq: D, Name: A, dtype: float64
```

选择通过 `[]`, 将行切片. 

```python
In [24]: df[0:3]
Out[24]: 
                   A         B         C         D
2013-01-01  0.469112 -0.282863 -1.509059 -1.135632
2013-01-02  1.212112 -0.173215  0.119209 -1.044236
2013-01-03 -0.861849 -2.104569 -0.494929  1.071804

In [25]: df['20130102':'20130104']
Out[25]: 
 A         B         C         D
2013-01-02  1.212112 -0.173215  0.119209 -1.044236
2013-01-03 -0.861849 -2.104569 -0.494929  1.071804
2013-01-04  0.721555 -0.706771 -1.039575  0.271860
```

#### 按标签选择

在[标签选择中](http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-label)查看更多信息. 

使用标签获取横截面：

```python
In [26]: df.loc[dates[0]]
Out[26]: 
A    0.469112
B   -0.282863
C   -1.509059
D   -1.135632
Name: 2013-01-01 00:00:00, dtype: float64
```

按标签选择多轴：

```python
In [27]: df.loc[:,['A','B']]
Out[27]: 
                   A         B
2013-01-01  0.469112 -0.282863
2013-01-02  1.212112 -0.173215
2013-01-03 -0.861849 -2.104569
2013-01-04  0.721555 -0.706771
2013-01-05 -0.424972  0.567020
2013-01-06 -0.673690  0.113648
```

显示标签切片, 两个端点*包括*：

```python
In [28]: df.loc['20130102':'20130104',['A','B']]
Out[28]: 
                   A         B
2013-01-02  1.212112 -0.173215
2013-01-03 -0.861849 -2.104569
2013-01-04  0.721555 -0.706771
```

减少返回对象的尺寸：

```python
In [29]: df.loc['20130102',['A','B']]
Out[29]: 
A    1.212112
B   -0.173215
Name: 2013-01-02 00:00:00, dtype: float64
```

获取标量值：

```python
In [30]: df.loc[dates[0],'A']
Out[30]: 0.46911229990718628
```

为了快速访问标量(相当于以前的方法)：

```python
In [31]: df.at[dates[0],'A']
Out[31]: 0.46911229990718628
```

#### 按位置选择

在[Position by Position中](http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-integer)查看更多信息. 

通过传递的整数的位置选择：

```python
In [32]: df.iloc[3]
Out[32]: 
A    0.721555
B   -0.706771
C   -1.039575
D    0.271860
Name: 2013-01-04 00:00:00, dtype: float64
```

通过整数切片, 类似于numpy / python：

```python
In [33]: df.iloc[3:5,0:2]
Out[33]: 
                   A         B
2013-01-04  0.721555 -0.706771
2013-01-05 -0.424972  0.567020
```

通过整数位置位置列表, 类似于numpy/python样式：

```python
In [34]: df.iloc[[1,2,4],[0,2]]
Out[34]: 
                   A         C
2013-01-02  1.212112  0.119209
2013-01-03 -0.861849 -0.494929
2013-01-05 -0.424972  0.276232
```

对于明确切片行：

```python
In [35]: df.iloc[1:3,:]
Out[35]: 
                   A         B         C         D
2013-01-02  1.212112 -0.173215  0.119209 -1.044236
2013-01-03 -0.861849 -2.104569 -0.494929  1.071804
```

对于明确切片列：

```python
In [36]: df.iloc[:,1:3]
Out[36]: 
                   B         C
2013-01-01 -0.282863 -1.509059
2013-01-02 -0.173215  0.119209
2013-01-03 -2.104569 -0.494929
2013-01-04 -0.706771 -1.039575
2013-01-05  0.567020  0.276232
2013-01-06  0.113648 -1.478427
```

为了明确获取值：

```python
In [37]: df.iloc[1,1]
Out[37]: -0.17321464905330858
```

为了快速访问标量(相当于以前的方法)：

```python
In [38]: df.iat[1,1]
Out[38]: -0.17321464905330858
```

#### 布尔索引

使用单个列的值来选择数据. 

```python
In [39]: df[df.A > 0]
Out[39]: 
                   A         B         C         D
2013-01-01  0.469112 -0.282863 -1.509059 -1.135632
2013-01-02  1.212112 -0.173215  0.119209 -1.044236
2013-01-04  0.721555 -0.706771 -1.039575  0.271860
```

从满足布尔条件的DataFrame中选择值. 

```python
In [40]: df[df > 0]
Out[40]: 
                   A         B         C         D
2013-01-01  0.469112       NaN       NaN       NaN
2013-01-02  1.212112       NaN  0.119209       NaN
2013-01-03       NaN       NaN       NaN  1.071804
2013-01-04  0.721555       NaN       NaN  0.271860
2013-01-05       NaN  0.567020  0.276232       NaN
2013-01-06       NaN  0.113648       NaN  0.524988
```

使用[`isin()`](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.isin.html#pandas.Series.isin "pandas.Series.isin")过滤方法：

```python
In [41]: df2 = df.copy()
In [42]: df2['E'] = ['one', 'one','two','three','four','three']
In [43]: df2
Out[43]: 
                   A         B         C         D      E
2013-01-01  0.469112 -0.282863 -1.509059 -1.135632    one
2013-01-02  1.212112 -0.173215  0.119209 -1.044236    one
2013-01-03 -0.861849 -2.104569 -0.494929  1.071804    two
2013-01-04  0.721555 -0.706771 -1.039575  0.271860  three
2013-01-05 -0.424972  0.567020  0.276232 -1.087401   four
2013-01-06 -0.673690  0.113648 -1.478427  0.524988  three
In [44]: df2[df2['E'].isin(['two','four'])]
Out[44]: 
                   A         B         C         D     E
2013-01-03 -0.861849 -2.104569 -0.494929  1.071804   two
2013-01-05 -0.424972  0.567020  0.276232 -1.087401  four
```

#### 设定

设置新列会自动根据索引对齐数据. 

```python
In [45]: s1 = pd.Series([1,2,3,4,5,6], index=pd.date_range('20130102', periods=6))
In [46]: s1
Out[46]: 
2013-01-02    1
2013-01-03    2
2013-01-04    3
2013-01-05    4
2013-01-06    5
2013-01-07    6
Freq: D, dtype: int64

In [47]: df['F'] = s1
```

按标签设置值：

```python
In [48]: df.at[dates[0],'A'] = 0
```

按位置设置值：

```python
In [49]: df.iat[0,1] = 0
```

通过使用NumPy数组进行设置：

```python
In [50]: df.loc[:,'D'] = np.array([5] * len(df))
```

先前设置操作的结果. 

```python
In [51]: df
Out[51]: 
                   A         B         C  D    F
2013-01-01  0.000000  0.000000 -1.509059  5  NaN
2013-01-02  1.212112 -0.173215  0.119209  5  1.0
2013-01-03 -0.861849 -2.104569 -0.494929  5  2.0
2013-01-04  0.721555 -0.706771 -1.039575  5  3.0
2013-01-05 -0.424972  0.567020  0.276232  5  4.0
2013-01-06 -0.673690  0.113648 -1.478427  5  5.0
```

一个`where`设置操作. 

```python
In [52]: df2 = df.copy()
In [53]: df2[df2 > 0] = -df2
In [54]: df2
Out[54]: 
                   A         B         C  D    F
2013-01-01  0.000000  0.000000 -1.509059 -5  NaN
2013-01-02 -1.212112 -0.173215 -0.119209 -5 -1.0
2013-01-03 -0.861849 -2.104569 -0.494929 -5 -2.0
2013-01-04 -0.721555 -0.706771 -1.039575 -5 -3.0
2013-01-05 -0.424972 -0.567020 -0.276232 -5 -4.0
2013-01-06 -0.673690 -0.113648 -1.478427 -5 -5.0
```

### 缺少数据

pandas主要使用该值`np.nan`来表示缺失的数据. 它默认不包含在计算中. 请参阅[缺失数据部分](http://pandas.pydata.org/pandas-docs/stable/missing_data.html#missing-data). 

重建索引允许您更改/添加/删除指定轴上的索引. 这将返回数据的副本. 

```python
In [55]: df1 = df.reindex(index=dates[0:4], columns=list(df.columns) + ['E'])
In [56]: df1.loc[dates[0]:dates[1],'E'] = 1
In [57]: df1
Out[57]: 
                   A         B         C  D    F    E
2013-01-01  0.000000  0.000000 -1.509059  5  NaN  1.0
2013-01-02  1.212112 -0.173215  0.119209  5  1.0  1.0
2013-01-03 -0.861849 -2.104569 -0.494929  5  2.0  NaN
2013-01-04  0.721555 -0.706771 -1.039575  5  3.0  NaN
```

删除任何缺少数据的行. 

```python
In [58]: df1.dropna(how='any')
Out[58]: 
                   A         B         C  D    F    E
2013-01-02  1.212112 -0.173215  0.119209  5  1.0  1.0
```

填写缺失的数据. 

```python
In [59]: df1.fillna(value=5)
Out[59]: 
                   A         B         C  D    F    E
2013-01-01  0.000000  0.000000 -1.509059  5  5.0  1.0
2013-01-02  1.212112 -0.173215  0.119209  5  1.0  1.0
2013-01-03 -0.861849 -2.104569 -0.494929  5  2.0  5.0
2013-01-04  0.721555 -0.706771 -1.039575  5  3.0  5.0
```

获取值所在的布尔掩码`nan`. 

```python
In [60]: pd.isna(df1)
Out[60]: 
                A      B      C      D      F      E
2013-01-01  False  False  False  False   True  False
2013-01-02  False  False  False  False  False  False
2013-01-03  False  False  False  False  False   True
2013-01-04  False  False  False  False  False   True
```

### 操作

请参阅[二进制运算](http://pandas.pydata.org/pandas-docs/stable/basics.html#basics-binop)的[基本部分](http://pandas.pydata.org/pandas-docs/stable/basics.html#basics-binop). 

#### 统计

操作通常*排除*丢失的数据. 

执行描述性统计：

```python
In [61]: df.mean()
Out[61]: 
A   -0.004474
B   -0.383981
C   -0.687758
D    5.000000
F    3.000000
dtype: float64
```

另一轴上的操作相同：

```python
In [62]: df.mean(1)
Out[62]: 
2013-01-01    0.872735
2013-01-02    1.431621
2013-01-03    0.707731
2013-01-04    1.395042
2013-01-05    1.883656
2013-01-06    1.592306
Freq: D, dtype: float64
```

使用具有不同维度的对象进行操作并需要对齐. 此外, pandas会自动沿指定维度进行广播. 

```python
In [63]: s = pd.Series([1,3,5,np.nan,6,8], index=dates).shift(2)
In [64]: s
Out[64]: 
2013-01-01    NaN
2013-01-02    NaN
2013-01-03    1.0
2013-01-04    3.0
2013-01-05    5.0
2013-01-06    NaN
Freq: D, dtype: float64

In [65]: df.sub(s, axis='index')
Out[65]: 
                   A         B         C    D    F
2013-01-01       NaN       NaN       NaN  NaN  NaN
2013-01-02       NaN       NaN       NaN  NaN  NaN
2013-01-03 -1.861849 -3.104569 -1.494929  4.0  1.0
2013-01-04 -2.278445 -3.706771 -4.039575  2.0  0.0
2013-01-05 -5.424972 -4.432980 -4.723768  0.0 -1.0
2013-01-06       NaN       NaN       NaN  NaN  NaN
```

#### apply

将函数应用于数据：

```python
In [66]: df.apply(np.cumsum)
Out[66]: 
                   A         B         C   D     F
2013-01-01  0.000000  0.000000 -1.509059   5   NaN
2013-01-02  1.212112 -0.173215 -1.389850  10   1.0
2013-01-03  0.350263 -2.277784 -1.884779  15   3.0
2013-01-04  1.071818 -2.984555 -2.924354  20   6.0
2013-01-05  0.646846 -2.417535 -2.648122  25  10.0
2013-01-06 -0.026844 -2.303886 -4.126549  30  15.0
In [67]: df.apply(lambda x: x.max() - x.min())
Out[67]: 
A    2.073961
B    2.671590
C    1.785291
D    0.000000
F    4.000000
dtype: float64
```

#### 直方图

在[直方图和离散化中](http://pandas.pydata.org/pandas-docs/stable/basics.html#basics-discretization)查看更多信息. 

```python
In [68]: s = pd.Series(np.random.randint(0, 7, size=10))
In [69]: s
Out[69]: 
0    4
1    2
2    1
3    2
4    6
5    4
6    4
7    6
8    4
9    4
dtype: int64
In [70]: s.value_counts()
Out[70]: 
4    5
6    2
2    2
1    1
dtype: int64
```

#### 字符串方法

Series在'str'属性中配备了一组字符串处理方法, 可以轻松地对数组的每个元素进行操作, 如下面的代码片段所示. 请注意, 'str'中的模式匹配通常默认使用[正则表达式](https://docs.python.org/3/library/re.html)(在某些情况下总是使用它们). 在[Vectorized String Methods中](http://pandas.pydata.org/pandas-docs/stable/text.html#text-string-methods)查看更多信息. 

```python
In [71]: s = pd.Series(['A', 'B', 'C', 'Aaba', 'Baca', np.nan, 'CABA', 'dog', 'cat'])
In [72]: s.str.lower()
Out[72]: 
0       a
1       b
2       c
3    aaba
4    baca
5     NaN
6    caba
7     dog
8     cat
dtype: object
```

### Merge

#### Concat

pandas提供了各种工具, 可以在连接/合并类型操作的情况下, 轻松地将Series, DataFrame和Panel对象与索引和关系代数功能的各种设置逻辑组合在一起. 

请参阅[合并部分](http://pandas.pydata.org/pandas-docs/stable/merging.html#merging). 

将pandas对象连接在一起[`concat()`](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.concat.html#pandas.concat "pandas.concat")：

```python
In [73]: df = pd.DataFrame(np.random.randn(10, 4))
In [74]: df
Out[74]: 
          0         1         2         3
0 -0.548702  1.467327 -1.015962 -0.483075
1  1.637550 -1.217659 -0.291519 -1.745505
2 -0.263952  0.991460 -0.919069  0.266046
3 -0.709661  1.669052  1.037882 -1.705775
4 -0.919854 -0.042379  1.247642 -0.009920
5  0.290213  0.495767  0.362949  1.548106
6 -1.131345 -0.089329  0.337863 -0.945867
7 -0.932132  1.956030  0.017587 -0.016692
8 -0.575247  0.254161 -1.143704  0.215897
9  1.193555 -0.077118 -0.408530 -0.862495
In [75]: pieces = [df[:3], df[3:7], df[7:]]
In [76]: pd.concat(pieces)
Out[76]: 
          0         1         2         3
0 -0.548702  1.467327 -1.015962 -0.483075
1  1.637550 -1.217659 -0.291519 -1.745505
2 -0.263952  0.991460 -0.919069  0.266046
3 -0.709661  1.669052  1.037882 -1.705775
4 -0.919854 -0.042379  1.247642 -0.009920
5  0.290213  0.495767  0.362949  1.548106
6 -1.131345 -0.089329  0.337863 -0.945867
7 -0.932132  1.956030  0.017587 -0.016692
8 -0.575247  0.254161 -1.143704  0.215897
9  1.193555 -0.077118 -0.408530 -0.862495
```

#### 加入

SQL样式合并. 请参阅[数据库样式连接](http://pandas.pydata.org/pandas-docs/stable/merging.html#merging-join)部分. 

```python
In [77]: left = pd.DataFrame({'key': ['foo', 'foo'], 'lval': [1, 2]})
In [78]: right = pd.DataFrame({'key': ['foo', 'foo'], 'rval': [4, 5]})
In [79]: left
Out[79]: 
 key  lval
0  foo     1
1  foo     2
In [80]: right
Out[80]: 
 key  rval
0  foo     4
1  foo     5
In [81]: pd.merge(left, right, on='key')
Out[81]: 
   key  lval  rval
0  foo     1     4
1  foo     1     5
2  foo     2     4
3  foo     2     5
```

另一个例子是：

```python
In [82]: left = pd.DataFrame({'key': ['foo', 'bar'], 'lval': [1, 2]})
In [83]: right = pd.DataFrame({'key': ['foo', 'bar'], 'rval': [4, 5]})
In [84]: left
Out[84]: 
 key  lval
0  foo     1
1  bar     2
In [85]: right
Out[85]: 
 key  rval
0  foo     4
1  bar     5
In [86]: pd.merge(left, right, on='key')
Out[86]: 
   key  lval  rval
0  foo     1     4
1  bar     2     5
```

#### 追加

将行附加到数据框. 请参阅“ [附加”](http://pandas.pydata.org/pandas-docs/stable/merging.html#merging-concatenation) 部分. 

```python
In [87]: df = pd.DataFrame(np.random.randn(8, 4), columns=['A','B','C','D'])
In [88]: df
Out[88]: 
          A         B         C         D
0  1.346061  1.511763  1.627081 -0.990582
1 -0.441652  1.211526  0.268520  0.024580
2 -1.577585  0.396823 -0.105381 -0.532532
3  1.453749  1.208843 -0.080952 -0.264610
4 -0.727965 -0.589346  0.339969 -0.693205
5 -0.339355  0.593616  0.884345  1.591431
6  0.141809  0.220390  0.435589  0.192451
7 -0.096701  0.803351  1.715071 -0.708758
In [89]: s = df.iloc[3]
In [90]: df.append(s, ignore_index=True)
Out[90]: 
          A         B         C         D
0  1.346061  1.511763  1.627081 -0.990582
1 -0.441652  1.211526  0.268520  0.024580
2 -1.577585  0.396823 -0.105381 -0.532532
3  1.453749  1.208843 -0.080952 -0.264610
4 -0.727965 -0.589346  0.339969 -0.693205
5 -0.339355  0.593616  0.884345  1.591431
6  0.141809  0.220390  0.435589  0.192451
7 -0.096701  0.803351  1.715071 -0.708758
8  1.453749  1.208843 -0.080952 -0.264610
```

### 分组

通过“分组依据”, 我们指的是涉及以下一个或多个步骤的过程：

* 根据某些标准将数据拆分为组
* 将功能独立应用于每个组
* 将结果**组合**到数据结构中

请参阅[分组部分](http://pandas.pydata.org/pandas-docs/stable/groupby.html#groupby). 

```python
In [91]: df = pd.DataFrame({'A' : ['foo', 'bar', 'foo', 'bar',
 ....:                          'foo', 'bar', 'foo', 'foo'],
 ....:                      'B' : ['one', 'one', 'two', 'three',
 ....:                             'two', 'two', 'one', 'three'],
 ....:                      'C' : np.random.randn(8),
 ....:                      'D' : np.random.randn(8)})
 ....: 
In [92]: df
Out[92]: 
     A      B         C         D
0  foo    one -1.202872 -0.055224
1  bar    one -1.814470  2.395985
2  foo    two  1.018601  1.552825
3  bar  three -0.595447  0.166599
4  foo    two  1.395433  0.047609
5  bar    two -0.392670 -0.136473
6  foo    one  0.007207 -0.561757
7  foo  three  1.928123 -1.623033
```

分组然后将[`sum()`](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.sum.html#pandas.DataFrame.sum "pandas.DataFrame.sum")函数应用于结果组. 

```python
In [93]: df.groupby('A').sum()
Out[93]: 
            C        D
A 
bar -2.802588  2.42611
foo  3.146492 -0.63958
```

按多列分组形成分层索引, 我们可以再次应用该`sum`功能. 

```python
In [94]: df.groupby(['A','B']).sum()
Out[94]: 
                  C         D
A   B 
bar one   -1.814470  2.395985
    three -0.595447  0.166599
    two   -0.392670 -0.136473
foo one   -1.195665 -0.616981
    three  1.928123 -1.623033
    two    2.414034  1.600434
```

### Reshaping

请参阅有关[分层索引](http://pandas.pydata.org/pandas-docs/stable/advanced.html#advanced-hierarchical)和 [重塑](http://pandas.pydata.org/pandas-docs/stable/reshaping.html#reshaping-stacking)的部分. 

#### 堆栈

```python
In [95]: tuples = list(zip(*[['bar', 'bar', 'baz', 'baz',
 ....:                        'foo', 'foo', 'qux', 'qux'],
 ....:                       ['one', 'two', 'one', 'two',
 ....:                        'one', 'two', 'one', 'two']]))
 ....: 
In [96]: index = pd.MultiIndex.from_tuples(tuples, names=['first', 'second'])
In [97]: df = pd.DataFrame(np.random.randn(8, 2), index=index, columns=['A', 'B'])
In [98]: df2 = df[:4]
In [99]: df2
Out[99]: 
                     A         B
first second 
bar   one     0.029399 -0.542108
      two     0.282696 -0.087302
baz   one    -1.575170  1.771208
      two     0.816482  1.100230
```

该[`stack()`](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.stack.html#pandas.DataFrame.stack "pandas.DataFrame.stack")方法“压缩”DataFrame列中的级别. 

```python
In [100]: stacked = df2.stack()
In [101]: stacked
Out[101]: 
first  second 
bar    one     A    0.029399
               B   -0.542108
       two     A    0.282696
               B   -0.087302
baz    one     A   -1.575170
               B    1.771208
       two     A    0.816482
               B    1.100230
dtype: float64
```

使用“堆叠”DataFrame或Series(具有`MultiIndex`as `index`), [`stack()`](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.stack.html#pandas.DataFrame.stack "pandas.DataFrame.stack")is 的逆操作, [`unstack()`](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.unstack.html#pandas.DataFrame.unstack "pandas.DataFrame.unstack")默认情况下取消堆叠**最后一级**：

```python
In [102]: stacked.unstack()
Out[102]: 
                     A         B
first second 
bar   one     0.029399 -0.542108
      two     0.282696 -0.087302
baz   one    -1.575170  1.771208
      two     0.816482  1.100230
In [103]: stacked.unstack(1)
Out[103]: 
second        one       two
first 
bar   A  0.029399  0.282696
      B -0.542108 -0.087302
baz   A -1.575170  0.816482
      B  1.771208  1.100230

In [104]: stacked.unstack(0)
Out[104]: 
first          bar       baz
second 
one    A  0.029399 -1.575170
       B -0.542108  1.771208
two    A  0.282696  0.816482
       B -0.087302  1.100230
```

#### 数据透视表

请参阅[数据透视表中](http://pandas.pydata.org/pandas-docs/stable/reshaping.html#reshaping-pivot)的部分. 

```python
In [105]: df = pd.DataFrame({'A' : ['one', 'one', 'two', 'three'] * 3,
 .....:                      'B' : ['A', 'B', 'C'] * 4,
 .....:                      'C' : ['foo', 'foo', 'foo', 'bar', 'bar', 'bar'] * 2,
 .....:                      'D' : np.random.randn(12),
 .....:                      'E' : np.random.randn(12)})
 .....: 
In [106]: df
Out[106]: 
        A  B    C         D         E
0     one  A  foo  1.418757 -0.179666
1     one  B  foo -1.879024  1.291836
2     two  C  foo  0.536826 -0.009614
3   three  A  bar  1.006160  0.392149
4     one  B  bar -0.029716  0.264599
5     one  C  bar -1.146178 -0.057409
6     two  A  foo  0.100900 -1.425638
7   three  B  foo -1.035018  1.024098
8     one  C  foo  0.314665 -0.106062
9     one  A  bar -0.773723  1.824375
10    two  B  bar -1.170653  0.595974
11  three  C  bar  0.648740  1.167115
```

我们可以非常轻松地从这些数据生成数据透视表：

```python
In [107]: pd.pivot_table(df, values='D', index=['A', 'B'], columns=['C'])
Out[107]: 
C             bar       foo
A     B 
one   A -0.773723  1.418757
      B -0.029716 -1.879024
      C -1.146178  0.314665
three A  1.006160       NaN
      B       NaN -1.035018
      C  0.648740       NaN
two   A       NaN  0.100900
      B -1.170653       NaN
      C       NaN  0.536826
```

### 时间序列

pandas具有简单, 强大且高效的功能, 用于在频率转换期间执行重采样操作(例如, 将第二数据转换为5分钟数据). 这在财务应用程序中非常常见, 但不仅限于此. 请参阅[时间序列部分](http://pandas.pydata.org/pandas-docs/stable/timeseries.html#timeseries). 

```python
In [108]: rng = pd.date_range('1/1/2012', periods=100, freq='S')
In [109]: ts = pd.Series(np.random.randint(0, 500, len(rng)), index=rng)
In [110]: ts.resample('5Min').sum()
Out[110]: 
2012-01-01    25083
Freq: 5T, dtype: int64
```

时区代表：

```python
In [111]: rng = pd.date_range('3/6/2012 00:00', periods=5, freq='D')
In [112]: ts = pd.Series(np.random.randn(len(rng)), rng)
In [113]: ts
Out[113]: 
2012-03-06    0.464000
2012-03-07    0.227371
2012-03-08   -0.496922
2012-03-09    0.306389
2012-03-10   -2.290613
Freq: D, dtype: float64
In [114]: ts_utc = ts.tz_localize('UTC')
In [115]: ts_utc
Out[115]: 
2012-03-06 00:00:00+00:00    0.464000
2012-03-07 00:00:00+00:00    0.227371
2012-03-08 00:00:00+00:00   -0.496922
2012-03-09 00:00:00+00:00    0.306389
2012-03-10 00:00:00+00:00   -2.290613
Freq: D, dtype: float64
```

转换为另一个时区：

```python
In [116]: ts_utc.tz_convert('US/Eastern')
Out[116]: 
2012-03-05 19:00:00-05:00    0.464000
2012-03-06 19:00:00-05:00    0.227371
2012-03-07 19:00:00-05:00   -0.496922
2012-03-08 19:00:00-05:00    0.306389
2012-03-09 19:00:00-05:00   -2.290613
Freq: D, dtype: float64
```

在时间跨度表示之间转换：

```python
In [117]: rng = pd.date_range('1/1/2012', periods=5, freq='M')
In [118]: ts = pd.Series(np.random.randn(len(rng)), index=rng)
In [119]: ts
Out[119]: 
2012-01-31   -1.134623
2012-02-29   -1.561819
2012-03-31   -0.260838
2012-04-30    0.281957
2012-05-31    1.523962
Freq: M, dtype: float64
In [120]: ps = ts.to_period()
In [121]: ps
Out[121]: 
2012-01   -1.134623
2012-02   -1.561819
2012-03   -0.260838
2012-04    0.281957
2012-05    1.523962
Freq: M, dtype: float64
In [122]: ps.to_timestamp()
Out[122]: 
2012-01-01   -1.134623
2012-02-01   -1.561819
2012-03-01   -0.260838
2012-04-01    0.281957
2012-05-01    1.523962
Freq: MS, dtype: float64
```

在周期和时间戳之间进行转换可以使用一些方便的算术函数. 在下面的示例中, 我们将季度频率与11月结束的年度转换为季度结束后的月末的上午9点：

```python
In [123]: prng = pd.period_range('1990Q1', '2000Q4', freq='Q-NOV')
In [124]: ts = pd.Series(np.random.randn(len(prng)), prng)
In [125]: ts.index = (prng.asfreq('M', 'e') + 1).asfreq('H', 's') + 9
In [126]: ts.head()
Out[126]: 
1990-03-01 09:00   -0.902937
1990-06-01 09:00    0.068159
1990-09-01 09:00   -0.057873
1990-12-01 09:00   -0.368204
1991-03-01 09:00   -1.144073
Freq: H, dtype: float64
```

### 分类

Pandas可以在`DataFrame`中包含分类数据. 有关完整文档, 请参阅 [分类简介](http://pandas.pydata.org/pandas-docs/stable/categorical.html#categorical)和[API文档](http://pandas.pydata.org/pandas-docs/stable/api.html#api-categorical). 

```python
In [127]: df = pd.DataFrame({"id":[1,2,3,4,5,6], "raw_grade":['a', 'b', 'b', 'a', 'a', 'e']})
```

将原始成绩转换为分类数据类型. 

```python
In [128]: df["grade"] = df["raw_grade"].astype("category")
In [129]: df["grade"]
Out[129]: 
0    a
1    b
2    b
3    a
4    a
5    e
Name: grade, dtype: category
Categories (3, object): [a, b, e]
```

将类别重命名为更有意义的名称(分配到 `Series.cat.categories`就位！). 

```python
In [130]: df["grade"].cat.categories = ["very good", "good", "very bad"]
```

重新排序类别并同时添加缺少的类别(默认情况下返回新方法). `Series .cat``Series`

```python
In [131]: df["grade"] = df["grade"].cat.set_categories(["very bad", "bad", "medium", "good", "very good"])
In [132]: df["grade"]
Out[132]: 
0    very good
1         good
2         good
3    very good
4    very good
5     very bad
Name: grade, dtype: category
Categories (5, object): [very bad, bad, medium, good, very good]
```

排序是按类别划分的每个订单, 而不是词汇顺序. 

```python
In [133]: df.sort_values(by="grade")
Out[133]: 
   id raw_grade      grade
5   6         e   very bad
1   2         b       good
2   3         b       good
0   1         a  very good
3   4         a  very good
4   5         a  very good
```

按分类列分组还显示空类别. 

```python
In [134]: df.groupby("grade").size()
Out[134]: 
grade
very bad     1
bad          0
medium       0
good         2
very good    3
dtype: int64
```

### 绘图

请参阅[绘图](http://pandas.pydata.org/pandas-docs/stable/visualization.html#visualization)文档. 

```python
In [135]: ts = pd.Series(np.random.randn(1000), index=pd.date_range('1/1/2000', periods=1000))
In [136]: ts = ts.cumsum()
In [137]: ts.plot()
Out[137]: <matplotlib.axes._subplots.AxesSubplot at 0x7f213444c048>
```

在DataFrame上, 该[`plot()`](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.plot.html#pandas.DataFrame.plot "pandas.DataFrame.plot")方法可以方便地使用标签绘制所有列：

```python
In [138]: df = pd.DataFrame(np.random.randn(1000, 4), index=ts.index,
 .....:                     columns=['A', 'B', 'C', 'D'])
 .....: 
In [139]: df = df.cumsum()
In [140]: plt.figure(); df.plot(); plt.legend(loc='best')
Out[140]: <matplotlib.legend.Legend at 0x7f212489a780>
```

### 获取数据进/出

#### CSV

[写入csv文件. ](http://pandas.pydata.org/pandas-docs/stable/io.html#io-store-in-csv)

```python
In [141]: df.to_csv('foo.csv')
```

[从csv文件中读取. ](http://pandas.pydata.org/pandas-docs/stable/io.html#io-read-csv-table)

```python
In [142]: pd.read_csv('foo.csv')
Out[142]: 
     Unnamed: 0          A          B         C          D
0    2000-01-01   0.266457  -0.399641 -0.219582   1.186860
1    2000-01-02  -1.170732  -0.345873  1.653061  -0.282953
2    2000-01-03  -1.734933   0.530468  2.060811  -0.515536
3    2000-01-04  -1.555121   1.452620  0.239859  -1.156896
4    2000-01-05   0.578117   0.511371  0.103552  -2.428202
5    2000-01-06   0.478344   0.449933 -0.741620  -1.962409
6    2000-01-07   1.235339  -0.091757 -1.543861  -1.084753
..          ...        ...        ...       ...        ...
993  2002-09-20 -10.628548  -9.153563 -7.883146  28.313940
994  2002-09-21 -10.390377  -8.727491 -6.399645  30.914107
995  2002-09-22  -8.985362  -8.485624 -4.669462  31.367740
996  2002-09-23  -9.558560  -8.781216 -4.499815  30.518439
997  2002-09-24  -9.902058  -9.340490 -4.386639  30.105593
998  2002-09-25 -10.216020  -9.480682 -3.933802  29.758560
999  2002-09-26 -11.856774 -10.671012 -3.216025  29.369368

[1000 rows x 5 columns]
```

#### HDF5

读写[HDFStores](http://pandas.pydata.org/pandas-docs/stable/io.html#io-hdf5). 

写入HDF5商店. 

```python
In [143]: df.to_hdf('foo.h5','df')
```

从HDF5商店阅读. 

```python
In [144]: pd.read_hdf('foo.h5','df')
Out[144]: 
                    A          B         C          D
2000-01-01   0.266457  -0.399641 -0.219582   1.186860
2000-01-02  -1.170732  -0.345873  1.653061  -0.282953
2000-01-03  -1.734933   0.530468  2.060811  -0.515536
2000-01-04  -1.555121   1.452620  0.239859  -1.156896
2000-01-05   0.578117   0.511371  0.103552  -2.428202
2000-01-06   0.478344   0.449933 -0.741620  -1.962409
2000-01-07   1.235339  -0.091757 -1.543861  -1.084753
...               ...        ...       ...        ...
2002-09-20 -10.628548  -9.153563 -7.883146  28.313940
2002-09-21 -10.390377  -8.727491 -6.399645  30.914107
2002-09-22  -8.985362  -8.485624 -4.669462  31.367740
2002-09-23  -9.558560  -8.781216 -4.499815  30.518439
2002-09-24  -9.902058  -9.340490 -4.386639  30.105593
2002-09-25 -10.216020  -9.480682 -3.933802  29.758560
2002-09-26 -11.856774 -10.671012 -3.216025  29.369368

[1000 rows x 4 columns]
```

#### Excel中

读写[MS Excel](http://pandas.pydata.org/pandas-docs/stable/io.html#io-excel). 

写入excel文件. 

```python
In [145]: df.to_excel('foo.xlsx', sheet_name='Sheet1')
```

从excel文件中读取. 

```python
In [146]: pd.read_excel('foo.xlsx', 'Sheet1', index_col=None, na_values=['NA'])
Out[146]: 
                    A          B         C          D
2000-01-01   0.266457  -0.399641 -0.219582   1.186860
2000-01-02  -1.170732  -0.345873  1.653061  -0.282953
2000-01-03  -1.734933   0.530468  2.060811  -0.515536
2000-01-04  -1.555121   1.452620  0.239859  -1.156896
2000-01-05   0.578117   0.511371  0.103552  -2.428202
2000-01-06   0.478344   0.449933 -0.741620  -1.962409
2000-01-07   1.235339  -0.091757 -1.543861  -1.084753
...               ...        ...       ...        ...
2002-09-20 -10.628548  -9.153563 -7.883146  28.313940
2002-09-21 -10.390377  -8.727491 -6.399645  30.914107
2002-09-22  -8.985362  -8.485624 -4.669462  31.367740
2002-09-23  -9.558560  -8.781216 -4.499815  30.518439
2002-09-24  -9.902058  -9.340490 -4.386639  30.105593
2002-09-25 -10.216020  -9.480682 -3.933802  29.758560
2002-09-26 -11.856774 -10.671012 -3.216025  29.369368

[1000 rows x 4 columns]
```

### 陷阱

如果您尝试执行操作, 您可能会看到如下异常：

```python
>>> if pd.Series([False, True, False]):
        print("I was true")
Traceback
 ...
ValueError: The truth value of an array is ambiguous. Use a.empty, a.any() or a.all().
```
