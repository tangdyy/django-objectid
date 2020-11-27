# Django-objectid

Django-objectid用于Django框架在分布式环境中高效生成不重复ID值。

### 依赖
+ django >= 2.2.0

### 安装
+ pip安装
```shell
pip install django-objectid
```
+ 源码安装
```shell
python setup.py install
```

### 使用
Django-objectid包括两个类，`ObjectID`，`ObjectidModel`。
##### class objectid.ObjectID(id=None)
生成、解析objectid。
参数id是一个长度为24的字符，如果是`None`则生成新的ObjectID实例，如果提供一个有效ID则解析这个ID为ObjectID实例。ObjectID实例有如下属性：
+ `timestamp`，ID中的时间戳，也就是ID创建的时间。 
+ `host`，ID中的主机名，是实际主机名经过哈希处理后的值。
+ `pid`，进程ID，可能与实际值不一致。
+ `count`，同一进程一秒内生成的ID序号。


```python
from objectid import ObjectID, create_objectid
# 创建ID对象
id = ObjectID()
# 获得id字符串
idstr = str(id)
# 直接创建id字符串
idstr = create_objectid()
# 解析id字符串
id = ObjectID('5fb1ee9af1d79721f0000015')
```
#### class objectid.ObjectidModel()
`ObjectidModel`是一个抽象类，不能单独使用，作为定义django模型类的基类。实例对象有如下属性和方法：
+ get_id_datetime()，返回id中的时间戳。

