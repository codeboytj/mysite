#  Django学习

Python2.7+Django1.8.2+djangorestframework3.6.3+Mysql

## 1. 环境搭建

### 1.1. 虚拟环境创建

基于python2.7创建名为helloDjango虚拟环境：
```
virtualenv helloDjango
```

这样，每个环境中的依赖包互不影响。然后使用命令进行虚拟环境：

```
source helloDjango/bin/activate
```
然后，就可以在环境中安装独立的依赖包了。

### 1.2. 一次性安装依赖

依赖全在requirements.txt中，直接安装依赖即可
```
pip install -r requirements.txt
```

### 1.3. 使用异步任务

打开celery的worker：

```
python manage.py celery worker --loglevel=info --settings=mysite.settings  --autoreload
```

使用django命令行执行异步任务：

```
from asyncTasks.hello import add
add.delay(4,5)
```

然后就可以在打开的worker中看到任务的运行状态了