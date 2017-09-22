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

### 1.2. 安装Django1.8.2

```
pip install Django==1.8.2
``` 

### 1.3. 使用Mysqldb与mysql进行交互

安装这个之前需要安装mysql，需要一些依赖
```
pip install MySQL-python==1.2.5
```

### 1.4. Django REST framework

#### 1.4.1. 环境搭建

安装djangorestframework
```
pip install djangorestframework==3.6.3
```
