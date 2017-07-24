---
title: Python-Basic-Model
date: 2017-07-24 09:13:47
categories: Python
tags: 
    - python
    - tutorial
---


# OS 操作系统接口

os模块的常用功能：

1.  os.name      #显示当前使用的平台
2.  os.getcwd()      #显示当前python脚本工作路径
3.  os.listdir('dirname')        #返回指定目录下的所有文件和目录名
4.  os.remove('filename')       #删除一个文件
5.  os.makedirs('dirname/dirname')     #可生成多层递规目录
6.  os.rmdir('dirname')     #删除单级目录
7.  os.rename("oldname","newname")    #重命名文件
8.  os.system()    #运行shell命令,注意：这里是打开一个新的shell，运行命令，当命令结束后，关闭shell
9.  os.sep    #显示当前平台下路径分隔符
10.  os.linesep    #给出当前平台使用的行终止符
11.  os.environ    #获取系统环境变量
12.  os.path.abspath(path)    #显示当前绝对路径
13.  os.path.dirname(path)    #返回该路径的父目录
14.  os.path.basename(path)    #返回该路径的最后一个目录或者文件,如果path以／或\结尾，那么就会返回空值。
15.  os.path.isfile(path)     #如果path是一个文件，则返回True
16.  os.path.isdir(path)    #如果path是一个目录，则返回True
17.  os.path.exists(path)    #如果path存在，则返回True
18.  os.path.split(path)  #将path分割成路径名和文件名。（事实上，如果你完全使用目录，它也会将最后一个目录作为文件名而分离，同时它不会判断文件或目录是否存在）
19.  os.path.join(path,name)   #连接目录与文件名或目录 结果为path/name


---

# sys 系统特定参数和函数

1.  sys.argv: 实现从程序外部向程序传递参数。
2.  sys.exit([arg]): 程序中间的退出，arg=0为正常退出。
3.  sys.getdefaultencoding(): 获取系统当前编码，一般默认为ascii。
4.  sys.setdefaultencoding(): 设置系统默认编码，执行dir（sys）时不会看到这个方法，在解释器中执行不通过，可以先执行reload(sys)，在执行 setdefaultencoding('utf8')，此时将系统默认编码设置为utf8。（见设置系统默认编码 ）
5.  sys.getfilesystemencoding(): 获取文件系统使用编码方式
6.  sys.path: 获取指定模块搜索路径的字符串集合，可以将写好的模块放在得到的某个路径下，就可以在程序中import时正确找到。
7.  sys.platform: 获取当前系统平台。
8.  sys.stdin,sys.stdout,sys.stderr: stdin , stdout , 以及stderr 变量包含与标准I/O 流对应的流对象. 如果需要更好地控制输出,而print 不能满足你的要求, 它们就是你所需要的. 你也可以替换它们, 这时候你就可以重定向输出和输入到其它设备( device ), 或者以非标准的方式处理它们


---

# random 产生随机数

1.  random.random()用于生成一个0到1的随机符点数
2.  random.uniform(a, b)，用于生成一个指定范围内的随机符点数
3.  random.randint(a, b)，用于生成一个指定范围内的整数
4.  random.randrange([start], stop[, step])，从指定范围内，按指定基数递增的集合中 获取一个随机数
5.  random.choice(sequence)从序列中获取一个随机元素
6.  random.shuffle(x[, random])，用于将一个列表中的元素打乱
7.  random.sample(sequence, k)，从指定序列中随机获取指定长度的片断
8.  random.seed() 方法改变随机数生成器的种子，可以在调用其他随机模块函数之前调用此函数


---

# pickle

1.  pickle.dumps(d),方法把任意对象序列化成一个bytes
2.  pickle.dump(f,d),直接把对象序列化后写入一个file-like Object
3.  pickle.loads(),方法反序列化出对象
4.  pickle.load(f),方法从一个file-like Object中直接反序列化出对象


---

# JSON 

1.  json.dump(obj, fp, *, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, cls=None, indent=None, separators=None, default=None, sort_keys=False, **kw),方法可以直接把JSON写入一个file-like Object
2.  json.dumps(),方法返回一个str，内容就是标准的JSON


要把JSON反序列化为Python对象，用`loads()`或者对应的`load()`方法，前者把JSON的字符串反序列化，后者从file-like Object中读取字符串并反序列化

