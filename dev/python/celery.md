目前我接触的`distributed task queue`比较有名的是python的celery和go的nsq, 本文是我在学习celery的一些总结

## Celery 是什么?
Celery是一个简单, 灵活, 可靠的分布式系统, 用于处理大量消息, 同时为操作提供维护此类系统所需的工具. 它是一个任务队列, 专注于实时处理, 同时还支持任务调度

## Celery 优点
- 简单: celery使用很简单, 你可以不用配置就可以启动一个任务
- 高度可用: worker和clients会自动处理失败或丢失的消息
- 快: 一个celery每分钟可以处理数百万的任务(使用RabbitMQ并做好优化) 
- 灵活: 几乎Celery的每个部分都可以自行扩展或使用, 自定义池实现, 序列化器, 压缩方案, 日志记录, 调度程序, 消费者, 生产者, 代理传输等等

## Celery 架构
![celery架构](https://upload-images.jianshu.io/upload_images/13148580-7967bc3bde8ac993.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

Broker: RabbitMQ, Redis
Backend: Redis, Memcached, SQLAlchemy, Cassandra, Elasticsearch
Concurrency: Prefork, Eventlet, Gevent
Serialization: Pickle, Json, Yaml, Zlib, Bzip2

## Celery 特性

### Monitoring 自检
+ Celery命令行(可以通过`celery <command> --help`了解celery的各种命令)
+ Flower是一个Django搭建的celery实时监测拓展
+ RabbitMQ(`rabbitmqctl list_queue`)和Redis, 查看各种broker和backend数据
+ 通过代码使用celery events跟踪任务
``` python
from celery import Celery

def my_monitor(app):
    state = app.events.State()

    def announce_failed_tasks(event):
        state.event(event)
        # task name is sent only with -received event, and state
        # will keep track of this for us.
        task = state.tasks.get(event['uuid'])

        print('TASK FAILED: %s[%s] %s' % (
            task.name, task.uuid, task.info(),))

    with app.connection() as connection:
        recv = app.events.Receiver(connection, handlers={
                'task-failed': announce_failed_tasks,  # 任务状态:处理函数
                '*': state.event,
        })
        recv.capture(limit=None, timeout=None, wakeup=True)

if __name__ == '__main__':
    app = Celery(broker='amqp://guest@localhost//')
    my_monitor(app)
```
### Scheduling 调度

`celery beat`是一个调度器, 它定期启动任务, 然后由群集中的可用工作节点执行

1. 将任务添加到节拍调度器 beat shedule

``` python
from celery import Celery
from celery.schedules import crontab

app = Celery()
app.conf.timezone =  'Asian/Shanghai'  # 需要设置时区, 默认是UTC,
app.conf.beat_schedule = {  # 配置中设置定时任务
    'add-every-30-seconds': {
        'task': 'tasks.add',
        'schedule': 30.0,  
        'schedule': crontab(hour=7, minute=30, day_of_week=1), 
        'schedule': solar('sunset', -37.81753, 144.96715),
        'args': (16, 16)
    },
}

@app.task
def add(a, b):
    return a + b

# 使用定时函数设置定时任务
@app.on_after_configure.connect  # 这个装饰器确保了配置完成后才调用函数
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')
    # Calls test('world') every 30 seconds
    sender.add_periodic_task(30.0, test.s('world'), expires=10)
    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        test.s('Happy Mondays!'),
    )

@app.task
def test(arg):
    print(arg)
```

2. 启动定时任务`celery -A proj beat`

### Work-Flows 任务流
`Signatures` : 包装单个任务调用的参数, 关键字参数和执行选项, 以便可以将其传递给函数, 甚至可以通过线路进行序列化和发送, 要使用signatures传递任务需要必须设置`result_backend`
``` python
s = add.s(2, 2, {'debug': True}).set(countdown=1)  # 星形参数的快捷方式, 通过set()函数定义options
s.args  # (2, 2)
s.kwargs  # {'debug': True}
s.options  # {'countdown': 10}

# Partial可以实现部分用于回调
s()  # 相当在当前进程执行add(2, 2)
s.delay()  # 相当在当前进程执行add.delay(2, 2)
s.apply_async()  # 相当在当前进程执行add.apply_asybc(2, 2)
p = add.s(2)  # 所有参数都可以在后续流程中传入
p.apply_async(args=(4,),kwargs={'debug': True}, countdown=1)

# Immutable不希望带上上一个任务的结果
add.apply_async((2, 2), link=reset_buffers.signature(immutable=True))
add.apply_async((2, 2), link=reset_buffers.si())
add.si(2, 3)  # 最好使用这个方式, 简单

# Callbacks可以用于任务回调
add.apply_async((2, 2), link=other_task.s())

# Chain 任务链式完成, 上一个结果可以用于后续任务
from celery import chain
res = chain(add.s(2, 2), add.s(4), add.s(8))()
res.get()  # 16
res1 = (add.s(2, 2) | add.s(4) | add.s(8))().get()  # 链式传递
res1.get()  # 16
res1.parent.get() # 8
res1.parent.parent.get()  # 4
res2 = (add.si(2, 2) | add.si(4, 8) | add.si(10, 10))()  # 结果不传递
res2.get()  # 20
res2.parent.get() # 12
res2.parent.parent.get()  # 4

# Group 创建一组要并行执行的任务
from celery import group
res = group(add.s(i, i) for i in xrange(10))()
res.get(timeout=1)  # [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

# Chord 所有任务完成执行时添加要调用的回调
from celery import chord
res = chord((add.s(i, i) for i in xrange(10)), xsum.s())()
res.get()  # 90

# Map he Chunk
xsum.map([range(10), range(100)])
res = add.chunks(zip(range(100), range(100)), 10)()
```

### Time & Rate Limits 时间评率限制
可以控制单个任务的请求评率和执行时间限制
``` python
# 时间限制有soft和hard之分, 运行超过soft会抛出SoftTimeLimitExceeded异常, 超过hard会直接终止任务, 可以在configuration中设置
task_soft_time_limit = 60
task_time_limit = 120
task_default_rate_limit = '200/m'

# 可以在任务中设置
@app.task(time_soft_limit=60 ,time_limit=120, rate_limit='200/m')
def test():
    pass

# 远程调用下面可以在运行中修改任务时间和评率限制
app.control.time_limit('tasks.crawl_the_web', soft=60, hard=120, reply=True)  
app.control.rate_limit('myapp.mytask', '200/m', destination=['celery@worker1.example.com'])  # destination可以指定相应节点限制评率
```

### Resource Leak Protection 资源泄露保护
可以通过设置来保护工作节点的资源不被泄露, 使用此选项, 您可以配置工作程序在被新进程替换之前可以执行的最大资源配置, 如果您无法控制资源使用, 例如来自闭源C扩展, 则此功能非常有用

- **Max tasks per child setting** 最大任务数, 可以使用workers [`--max-tasks-per-child`]
- **Max memory per child** 最大内存, 可以使用workers [`--max-memory-per-child`]

``` python
# 池工作进程在用新工作进程替换之前可以执行的最大任务数, 默认是没有限制的
worker_max_tasks_per_child = 10
# 在新worker替换之前，worker可能消耗的最大驻留内存量, 如果单个任务导致worker超过此限制, 则任务将完成，worker将被替换
worker_max_memory_per_child = 12000  # 12MB
```

### User Components 用户组件

可以定制每个工作组件, 并且可以由用户定义其他组件. 工作人员使用“bootsteps”构建 - 一个依赖关系图, 可以对工人的内部进行细粒度控制
