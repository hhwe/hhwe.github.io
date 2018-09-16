## Application 应用
Celery库必须在使用前进行实例化, 此实例称为应用程序(或简称app). 该应用程序是线程安全的, 因此具有不同配置, 组件和任务的多个Celery应用程序可以在同一个进程空间中共存
``` python
from celery import Celery
app = Celery('tasks')  # 在使用的时候最好指定应用名

app.conf.timezone = 'Asian/Shanghai'  # 运行中配置
import celeryconfig 
app.config_from_object(celeryconfig)  # 最常见的配置形式, 从配置模块中读取配置
app.config_from_envvar('CELERY_CONFIG_MODULE')  # 从环境变量中读取配置

# 打印app配置, 可以将私密信息做屏蔽
app.conf.humanize(with_defaults=False, censored=True)
app.conf.table(with_defaults=False, censored=True)  # dict形式

@app.task(queue='hipri', name='tasks.add', bind=DebugTask)  # 直接装饰器上绑定任务
def add(x, y): 
    return x + y

from celery.task import Task
from celery.registry import tasks
class Hello(Task):
    queue = 'hipri'
    name = 'tasks.add'
    bind = DebugTask
    def run(self, to):
        return 'hello {0}'.format(to)
tasks.register(Hello)   # 通过注册形式绑定到app

from celery import Task  # 所有的task都是一个Task类实例
class DebugTask(Task):
    def __call__(self, *args, **kwargs):  # 每次任务响应会调用该方法
        print('TASK STARTING: {0.name}[{0.request.id}]'.format(self))
        return super(DebugTask, self).__call__(*args, **kwargs)

if __name__ == '__main__':
    app.worker_main()
```

# Tasks 任务
任务是Celery应用程序的构建块, 是可以从任何地方调用的类. 它执行双重角色, 因为它定义了调用任务时发生的事情(发送消息), 以及当worker收到该消息时会发生什么.
每个任务类都有一个唯一的名称, 并且在消息中引用此名称, 以便worker可以找到要执行的正确函数. 
在worker确认该消息之前, 不会从队列中删除任务消息. worker可以提前预订许多消息, 即使worker因电源故障或其他原因被杀, 该消息也会被重新传递给另一worker
``` python
import celery

class MyTask(celery.Task):
    queue = 'add'
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('{0!r} failed: {1!r}'.format(task_id, exc))

# 最好每个自定义一个name, 如果使用默认会有模块导入问题
@task(bind=True, base=MyTask, name='tasks.add')
def add(self, x, y):
    print('Executing task id {0.id}, args: {0.args!r} kwargs: {0.kwargs!r}'.format(self.request))
    return x + y

# retry可用于重新执行任务
@app.task(autoretry_for=(FailWhaleError,), retry_kwargs={'max_retries': 5})
def refresh_timeline(user):
    try:
        twitter.refresh_timeline(user)
    except FailWhaleError as exc:
        raise div.retry(exc=exc, max_retries=5)
```

