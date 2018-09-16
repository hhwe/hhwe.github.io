### 批量删除进程

有时候因为一些情况，需要把 linux 下符合某一项条件的所有进程 kill 掉，又不能用 killall 直接杀掉某一进程名称包含的所有运行中进程（我们可能只需要杀掉其中的某一类或运行指定参数命令的进程）
1. 运用 ps, grep, cut 和 kill 一起操作。管道符"|"用来隔开两个命令，管道符左边命令的输出会作为管道符右边命令的输入
```
ps -ef | grep xxx | grep -v grep | cut -c 9-15 | xargs kill -9
"ps -ef" 是linux里查看所有进程的命令。这时检索出的进程将作为下一条命令"grep xxx"的输入
"grep xxx" 的输出结果是，所有含有关键字"xxx"的进程
"grep -v grep" 是在列出的进程中去除含有关键字"grep"的进程
"cut -c 9-15" 是截取输入行的第9个字符到第15个字符，而这正好是进程号PID
"xargs kill -9" 中的 xargs 命令是用来把前面命令的输出结果（PID）作为"kill -9"命令的参数，并执行该命令。"kill -9"会强行杀掉指定进程
其它类似的情况，只需要修改"grep xxx"中的关键字部分就可以了
```
2. 使用awk
`awk` 命令远比`grep`命令强大, 让我想起python中的`%`和`format`函数
```
ubuntu@ubuntu:~$ ps -ef | awk '{printf "%-8s %-8s %-8s %-18s %-22s %-15s\n",$1,$2,$3,$4,$5,$6}'  // 打印相关列信息
UID      PID      PPID     C                  STIME                  TTY
root     1        0        0                  Aug16                  ?
root     2        0        0                  Aug16                  ?

ubuntu@ubuntu:~$ ps -ef | awk '$3>1000'  // 条件过滤
UID        PID  PPID  C STIME TTY          TIME CMD
www-data  1092  1091  0 Aug16 ?        00:00:00 nginx: worker process
ubuntu    2361  2358  0 Aug17 ?        00:00:00 (sd-pam)
root     17531  1006  0 14:02 ?        00:00:00 sshd: ubuntu [priv]
ubuntu   17585 17531  0 14:02 ?        00:00:00 sshd: ubuntu@pts/1

ps x|grep gas|grep -v grep |awk '{print $1}'|xargs kill -9
```


## 防火墙和端口设置

```
sudo ufw enable/disable  // 打开/关闭防火墙
sudo ufw allow/deny 1080  // 暴露/拒绝1080端口
```

## tar在打包时候差异
```
tar --dereference -czvf dist/owlscrapy.tar.gz --exclude='*.pyc' --exclude='*.pyo' tasks  # 注意在mac下--exclude必须在目标文件前面,  linux下无所谓前后
```
## eval 
eval会对后面的cmdLine进行两遍扫描，如果第一遍扫描后，cmdLine是个普通命令，则执行此命令；如果cmdLine中含有变量的间接引用，则保证间接引用的语义。
 
```
set 11 22 33 44  
# 如果要输出最近一个参数，即44，可以使用如下命令，
echo $4  # 44
# 但是如果我们不知道有几个参数的时候，要输出最后一个参数，大家可能会想到使用$#来输出最后一个参数，
# 如果使用命令：
echo "\$$#"  # $4
# 则得到的结果是 $4，而不是我们想要的44。这里涉及到一个变量间接引用的问题，我们的本意是输出 $4，默认情况下，命令后忽略变量间接引用的情况。
# 这时候，就可以使用eval命令。
eval echo "\$$#"  # 44
```
