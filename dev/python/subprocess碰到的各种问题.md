Python 标准库 subprocess.Popen 是 shellout 一个外部进程的首选，它在 Linux/Unix 平台下的实现方式是 fork 产生子进程然后 exec 载入外部可执行程序。

于是问题就来了，如果我们需要一个类似“夹具”的子进程（比如运行 Web 集成测试的时候跑起来的那个被测试 Server）， 那么就需要在退出上下文的时候清理现场，也就是结束被跑起来的子进程。

最简单粗暴的做法可以是这样：
根据subprocess启动的子线程pid, 使用shell脚本杀掉所有子孙先

这个问题稍微有点棘手，因为自从被运行程序 fork 以后，产生的子进程都享有独立的进程空间和 pid，也就是它超出了我们触碰的范围。好在 subprocess.Popen 有个 preexec_fn 参数，它接受一个回调函数，并在 fork 之后 exec 之前的间隙中执行它。我们可以利用这个特性对被运行的子进程做出一些修改，比如执行 setsid() 成立一个独立的进程组。

Linux 的进程组是一个进程的集合，任何进程用系统调用 setsid 可以创建一个新的进程组，并让自己成为首领进程。首领进程的子子孙孙只要没有再调用 setsid 成立自己的独立进程组，那么它都将成为这个进程组的成员。 之后进程组内只要还有一个存活的进程，那么这个进程组就还是存在的，即使首领进程已经死亡也不例外。 而这个存在的意义在于，我们只要知道了首领进程的 pid (同时也是进程组的 pgid)， 那么可以给整个进程组发送 signal，组内的所有进程都会收到。

因此利用这个特性，就可以通过 preexec_fn 参数让 Popen 成立自己的进程组， 然后再向进程组发送 SIGTERM 或 SIGKILL，中止 subprocess.Popen 所启动进程的子子孙孙。当然，前提是这些子子孙孙中没有进程再调用 setsid 分裂自立门户。

前文的例子经过修改是这样的：

better_process_fixture.py
```
 import signal
 import os
 import contextlib
 import subprocess
 import logging
 import warnings


 @contextlib.contextmanager
 def process_fixture(shell_args):
     proc = subprocess.Popen(shell_args, preexec_fn=os.setsid)
     try:
         yield
     finally:
         proc.terminate()
         proc.wait()

         try:
             os.killpg(proc.pid, signal.SIGTERM)
         except OSError as e:
             warnings.warn(e)
```
Python 3.2 之后 subprocess.Popen 新增了一个选项 start_new_session， Popen(args, start_new_session=True) 即等效于 preexec_fn=os.setsid 。

这种利用进程组来清理子进程的后代的方法，比简单地中止子进程本身更加“干净”。基于 Python 实现的 Procfile 进程管理工具 Honcho 也采用了这个方法。当然，因为不能保证被运行进程的子进程一定不会调用 setsid， 所以这个方法不能算“通用”，只能算“相对可用”。如果真的要百分之百通用，那么像 systemd 那样使用 cgroups 来追溯进程创建过程也许是唯一的办法。也难怪说 systemd 是第一个能正确地关闭服务的 init 工具。

## Linux的进程相互之间有一定的关系
比如说，在[Linux进程基础](http://www.cnblogs.com/vamei/archive/2012/09/20/2694466.html)中，我们看到，每个进程都有父进程，而所有的进程以init进程为根，形成一个树状结构。我们在这里讲解进程组和会话，以便以更加丰富的方式了管理进程。

### 进程组 (process group)

每个进程都会属于一个进程组(process group)，每个进程组中可以包含多个进程。进程组会有一个进程组领导进程 (process group leader)，领导进程的PID (PID见[Linux进程基础](http://www.cnblogs.com/vamei/archive/2012/09/20/2694466.html))成为进程组的ID (process group ID, PGID)，以识别进程组。
```
$ps -o pid,pgid,ppid,comm | cat
PID  PGID  PPID COMMAND
17763 17763 17751 bash
18534 18534 17763 ps
18535 18534 17763 cat</pre>
```
PID为进程自身的ID，PGID为进程所在的进程组的ID， PPID为进程的父进程ID。从上面的结果，我们可以推测出如下关系：

![image](http://upload-images.jianshu.io/upload_images/13148580-56b03d609acded45.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240) 

图中箭头表示父进程通过[fork和exec机制](http://www.cnblogs.com/vamei/archive/2012/09/20/2694466.html)产生子进程。ps和cat都是bash的子进程。进程组的领导进程的PID成为进程组ID。领导进程可以先终结。此时进程组依然存在，并持有相同的PGID，直到进程组中最后一个进程终结。

我们将一些进程归为进程组的一个重要原因是我们可以将[信号](http://www.cnblogs.com/vamei/archive/2012/10/04/2711818.html)发送给一个进程组。进程组中的所有进程都会收到该信号。我们会在下一部分深入讨论这一点。

### 会话 (session)

更进一步，在shell支持工作控制(job control)的前提下，多个进程组还可以构成一个会话 (session)。bash(Bourne-Again shell)支持工作控制，而sh(Bourne shell)并不支持。

会话是由其中的进程建立的，该进程叫做会话的领导进程(session leader)。会话领导进程的PID成为识别会话的SID(session ID)。会话中的每个进程组称为一个工作(job)。会话可以有一个进程组成为会话的前台工作(foreground)，而其他的进程组是后台工作(background)。每个会话可以连接一个控制终端(control terminal)。当控制终端有输入输出时，都传递给该会话的前台进程组。由终端产生的信号，比如CTRL+Z， CTRL+\，会传递到前台进程组。

会话的意义在于将多个工作囊括在一个终端，并取其中的一个工作作为前台，来直接接收该终端的输入输出以及终端信号。 其他工作在后台运行。

一个命令可以通过在末尾加上&方式让它在后台运行:
```
$ping localhost > log &  # [1] 10141括号中的1表示工作号，而10141为PGID
$ps -o pid,pgid,ppid,sid,tty,comm  # (tty表示控制终端）
$kill -SIGTERM -10141
$kill -SIGTERM %1
```
的方式来发送给工作组。上面的两个命令，一个是发送给PGID(通过在PGID前面加-来表示是一个PGID而不是PID)，一个是发送给工作1(%1)，两者等价。

一个工作可以通过`$fg`从后台工作变为前台工作:
```
$cat > log &
$fg %1
```
当我们运行第一个命令后，由于工作在后台，我们无法对命令进行输入，直到我们将工作带入前台，才能向cat命令输入。在输入完成后，按下CTRL+D来通知shell输入结束。 

进程组(工作)的概念较为简单易懂。而会话主要是针对一个终端建立的。当我们打开多个终端窗口时，实际上就创建了多个终端会话。每个会话都会有自己的前台工作和后台工作。这样，我们就为进程增加了管理和运行的层次。在没有图形化界面的时代，会话允许用户通过shell进行多层次的进程发起和管理。比如说，我可以通过shell发起多个后台工作，而此时标准输入输出并不被占据，我依然可以继续其它的工作。如今，图形化界面可以帮助我们解决这一需求，但工作组和会话机制依然在Linux的许多地方应用。 

### 总结 
process group, pgid 
session, sid, job, forground, background
fg, kill -pid, &, %
