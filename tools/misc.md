# 开发总结

## python

### python源环境

python独立运行环境
```
python -m venv .venv
```

### 替换python源

三种方式

1. pip config set global.index-utl https://pypi.mirrors.ustc.edu.cn/simple/
2. pip install pands -i https://pypi.mirrors.ustc.edu.cn/simple/
3. vim ~/.config/pip/pip.conf

国内python开源镜像站

```
豆瓣：http://pypi.douban.com/simple/
中科大：https://pypi.mirrors.ustc.edu.cn/simple/
清华：https://pypi.tuna.tsinghua.edu.cn/simple/
阿里云：https://mirrors.aliyun.com/pypi/simple/
```

