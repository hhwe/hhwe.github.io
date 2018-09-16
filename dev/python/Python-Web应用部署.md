python的web应用部署方式本人在项目中使用过的:
+ flask + gunicorn + supervisor + nginx
+ docker

### 实现一个flask应用
``` python
# app.py
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'hello world'
```
使用flask自带的wsgi(适合测试使用)启动
``` sh
flask run
```

### 使用gunicorn启动
``` pyhton
# gunicorn.conf.py
import multiprocessing
workers = multiprocessing.cpu_count() * 2 + 1  # --workers=5
workers_class = "gevent"  # --workers-class=gevent
bind = "0.0.0.0:7070"  # --bind=:7070
reload = True  # --reload=True 代码改动后自动重启
accesslog = "/home/ubuntu/flaskapp/logs/gunicorn_access.log"
errorlog = "/home/ubuntu/flaskapp/logs/gunicorn_error.log"
```
可以使用gunicorn命令启动运行
``` sh
gunicorn app:app -c gunicorn.conf.py 
```

### supervisor管理应用进程
``` conf
[program:gunicorn]
command=/path/to/gunicorn main:application -c /path/to/gunicorn.conf.py
directory=/path/to/project
user=nobody
autostart=true
autorestart=true
redirect_stderr=true
# 特别注意需在字符中有%号需要通过%号转义%%
environment=SQLALCHEMY_DATABASE_URI = "mysql+pymysql://*%%*:**@**/test?charset=utf8",REDIS_URL="redis://**/11" 
stdout_logfile=/home/ubuntu/flaskapp/logs/supervisor_out.log
stderr_logfile=/home/ubuntu/flaskapp/logs/supervisor_err.log
```
通过supervisorctl管理进程
``` sh
sudo supervisorctl reload
```

### 使用nginx做服务器
``` conf
upstream host_name.com {
    ip_hash;  // *2*
    server example1.com weight=4; // *4*, 默认权重为1
    server example2.com backup; //备机,不能和ip_hash关键字一起使用
    server example3.com max_fails=3 fail_timeout=30s; //指定最大的重试次数，和重试时间间隔
}
#Nginx负载均衡有4种方案配置:
#1. 轮询,配置文件中的顺序,依次把客户端的Web请求分发到不同的后端服务器上
#2. 最少连接, Web请求会被转发到连接数最少的服务器上
#3. IP地址哈希,前述的两种负载均衡方案中, 同一客户端连续的Web请求可能会被分发到不同的后端服务器进行处理, 因此如果涉及到会话Session, 那么会话会比较复杂. 常见的是基于数据库的会话持久化. 要克服上面的难题, 可以使用基于IP地址哈希的负载均衡方案. 这样的话, 同一客户端连续的Web请求都会被分发到同一服务器进行处理
#4. 基于权重, 请求更多地分发到高配置的后端服务器上, 把相对较少的请求分发到低配服务器
server {
    listen 80;
    server_name host_name.com;

    location / {
        proxy_pass http://host_name.com;
    }
}
```
nginx可以作为反向代理和负载均衡的web服务器, gunicorn官网推荐使用nginx作为反向代理服务器
``` sh
sudo service nginx start
```

### docker容器部署
``` dockerfile
FROM python:3
WORKDIR $HOME/flaskapp
COPY . .
RUN pip install -r requirements.txt
CMD ["gunicorn", "app:app", "-c", "gunicorn.conf.py"]
```
docker可以将部署环境搭建在容器中, 使用起来相当方便, 只需一个Dockefile文件, 再执行docker build创建image, 然后运行image
``` sh
docker build -t 'flaskapp:v1' .
docker run 80:5000 flaskapp:v1
```
