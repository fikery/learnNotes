# 1.python中一切皆对象
python中类和函数都是对象，属于python的一等公民。具体表现在：
1. 可以赋值给一个变量
2. 可以添加到集合当中
3. 可以作为函数的参数
4. 可以作为函数的返回值

**type object class之间的关系**
```
a = 1
b = 'abc'
type(a)  # <class 'int'>
type(int)  # <class 'type'>
type(b)  # <class 'str'>
type(str)  # <class 'type'>

从这里我们可以看到生成关系type->class->obj
可以得出结论，一般对象是由类生成的，而类是由type生成的
```

```
object.__bases__  # ()
type.__bases__  # (<class 'object'>,)
type(object)  # <class 'type'>

object是顶层基类，type也是一个类
type类的基类是object
object类是由type类生成的
```
普通对象'abc'是str类的实例对象，str/int/set/dict/tuple等都是type类的实例对象，type类是type类自身的实例对象，而他们所有都继承自object类。但是需要注意的是⚠️object类也是type类的实例对象。因此python中一切皆对象，而对象都是可以修改的。

python中的对象有3个特征：身份/id、类型/type、值/value。

python中常见的内置类型：None(全局唯一)，迭代类型，序列类型(list/tuple/str/bytes等),映射类型(dict)，集合类型，上下文管理器类型(with),其他类型(模块类型/实例类型/方法类型等)

# python中的魔法函数
* python中以双下划线开头和结尾的函数，称为魔法函数
* 以单下划线开头表示不是API的一部分，不提供对外访问(虽然直接访问也没有问题)
* 以双下划线开头表示不能重写该方法，重写无效，不能直接访问(可以通过_className__method()来访问)
* 以双下划线开头结尾表示是python自己内置调用的，不要直接调用

如__getitem__实现可迭代对象，__iter__实现迭代器，迭代一个对象时，会先找__iter__，如果没有实现就找__getitem__。

len()函数会查找是否实现了__len__，print()函数会先找__str__是否实现，如果没有就找__repr__。

还有其他很多数学运算函数，比如__abs__以及__sum__还有__add__等。


