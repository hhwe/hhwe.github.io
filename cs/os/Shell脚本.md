
### 变量
``` sh
#!/bin/bash

# 定义变量时，变量名不加美元符号:
a="variable"  # 变量名和等号之间不能有空格

# 除了显式地直接赋值，还可以用语句给变量赋值

for file in `ls /etc`
for file in $(ls /etc)

# 使用一个定义过的变量，只要在变量名前面加美元符号 `$` 即可
echo $a
echo ${a}

# 使用 `readonly` 命令可以将变量定义为只读变量，只读变量的值不能被改变。
myVar="xxx"
readonly myVar
myVar="xxx"  # /bin/sh: NAME: This variable is read only.

# 删除变量，使用 `unset` 命令可以删除变量
unset a
```

### 字符串
``` sh
# !/bin/bash
a="string"
# 单引号里的任何字符都会原样输出，单引号字符串中的变量是无效的
str='this is a $a'  
echo $str  # this is a $a
# 双引号里可以有变量，双引号里可以出现转义字符
str="this is a $a"
echo $str  # this is a string

string="abcdefg"
# 获取字符串长度
echo ${#string}  # 7
# 提取子字符串
echo ${string:2:4}  # cdef
```

### 数组
```
arr=(1 2 3 4 5)
arr=(
1
2
3
4
5
)
echo arr[6]=6
echo ${arr[@]}
# 取得数组元素的个数
echo length=${#arr[@]}  # length=5
echo length=${#arr[*]}  # length=5


# 取得数组单个元素的长度
echo lengthn=${#arr[n]}  # lengthn=1
```

### 传参
特殊字符用来处理参数
| 参数处理 | 说明 |
| --- | --- |
| $# | 传递到脚本的参数个数 |
| $* | 以一个单字符串显示所有向脚本传递的参数。如"$*"用「"」括起来的情况、以"$1 $2 … $n"的形式输出所有参数。 |
| $$ | 脚本运行的当前进程ID号 |
| $! | 后台运行的最后一个进程的ID号 |
| $@ | 与$*相同，但是使用时加引号，并在引号中返回每个参数。如"$@"用「"」括起来的情况、以"$1" "$2" … "$n" 的形式输出所有参数。 |
| $- | 显示Shell使用的当前选项，与[set命令](http://www.runoob.com/linux/linux-comm-set.html)功能相同。 |
| $? | 显示最后命令的退出状态。0表示没有错误，其他任何值表明有错误。 |

原生bash不支持简单的数学运算，但是可以通过其他命令来实现，例如 `awk` 和 `expr`，`expr` 最常用。

`expr` 是一款表达式计算工具，使用它能完成表达式的求值操作: 
```
#!/bin/bash
echo `expr 2 + 2`  # 4
```

### 函数

linux shell 可以用户定义函数，然后在shell脚本中可以随便调用。

shell中函数的定义格式如下：

[ function ] funname [()]

{

    action;

    [return int;]

}
说明：

1、可以带function fun() 定义，也可以直接fun() 定义,不带任何参数。
2、参数返回，可以显示加：return 返回，如果不加，将以最后一条命令运行结果，作为返回值。 return后跟数值n(0-255
下面的例子定义了一个函数并进行调用：
```
#!/bin/bash
demoFun(){
    echo "abc"
}
demoFun  # abc

funWithReturn(){
    echo "这个函数会对输入的两个数字进行相加运算..."
    echo "输入第一个数字: "
    read aNum
    echo "输入第二个数字: "
    read anotherNum
    echo "两个数字分别为 $aNum 和 $anotherNum !"
    return $(($aNum+$anotherNum))
}
funWithReturn  # 返回值用$?来获得
echo "输入的两个数字之和为 $? !"

# 在Shell中，调用函数时可以向其传递参数。在函数体内部，通过 $n 的形式来获取参数的值，例如，$1表示第一个参数，$2表示第二个参数...
funWithParam(){
    echo "第一个参数为 $1 !"
    echo "第二个参数为 $2 !"
    echo "第十个参数为 $10 !"
    echo "第十个参数为 ${10} !"
    echo "第十一个参数为 ${11} !"
    echo "参数总数有 $# 个!"
    echo "作为一个字符串输出所有参数 $* !"
}
funWithParam 1 2 3 4 5 6 7 8 9 34 73 # 
```



