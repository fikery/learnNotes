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
```
从这里我们可以看到生成关系type->class->obj

可以得出结论，一般对象是由类生成的，而类是由type生成的

```
object.__bases__  # ()
type.__bases__  # (<class 'object'>,)
type(object)  # <class 'type'>
```
object是顶层基类，type也是一个类

type类的基类是object

object类是由type类生成的

