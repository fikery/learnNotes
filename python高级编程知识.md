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
print(type(a))  # <class 'int'>
print(type(int))  # <class 'type'>
print(type(b))  # <class 'str'>
print(type(str))  # <class 'type'>

# 从这里我们可以看到生成关系type->class->obj
# 可以得出结论，一般对象是由类生成的，而类是由type生成的
```

```
print(object.__bases__) # ()
print(type.__bases__) # (<class 'object'>,)
print(type(object))  # <class 'type'>

# object是顶层基类，type也是一个类
# type类的基类是object
# object类是由type类生成的
```
普通对象'abc'是str类的实例对象，str/int/set/dict/tuple等都是type类的实例对象，type类是type类自身的实例对象，而他们所有都继承自object类。但是需要注意的是⚠️object类也是type类的实例对象。因此python中一切皆对象，而对象都是可以修改的。

python中的对象有3个特征：身份/id、类型/type、值/value。

python中常见的内置类型：None(全局唯一)，迭代类型，序列类型(list/tuple/str/bytes等),映射类型(dict)，集合类型，上下文管理器类型(with),其他类型(模块类型/实例类型/方法类型等)

# 2.python中的魔法函数
* python中以双下划线开头和结尾的函数，称为魔法函数
* 以单下划线开头表示不是API的一部分，不提供对外访问(虽然直接访问也没有问题)
* 以双下划线开头表示不能重写该方法，重写无效，不能直接访问(可以通过_className__method()来访问)
* 以双下划线开头结尾表示是python自己内置调用的，不要直接调用

如__getitem__实现可迭代对象，而__iter__实现迭代器，迭代一个对象时，会先找__iter__，如果没有实现就找__getitem__。

还有len()函数会查找是否实现了__len__，另外print()函数会先找__str__是否实现，如果没有就找__repr__。

还有其他很多数学运算函数，比如__abs__以及__sum__还有__add__等。
```
class A:
    def __init__(self, lst):
        self.lst = lst

    # 魔法方法，使得A的实例对象成为可迭代对象，也成为了序列类型
    def __getitem__(self, item):
        return self.lst[item]
2.
    # 可以获取传入列表的长度
    def __len__(self):
        return len(self.lst)

    # 格式化输出的对象
    def __str__(self):
        return ','.join(self.lst)

    # 开发模式的原始对象
    def __repr__(self):
        return ','.join(self.lst)


a = A(['x', 'y', 'z'])

# __getitem__实现序列类型，可切片
print(a[:2])
# __getitem__直接迭代a对象，而不是a.lst
for i in a:
    print(i)
# 实际调用__len__
print(len(a))
# 没有实现__repr__时
print(repr(a))  # <__main__.A object at 0x10c304a90>
# 实现了__repr__时
print(repr(a))  # x,y,z
# 没有实现__str__和__repr__时
print(a)  # <__main__.A object at 0x10e897a90>
# 实现了__str__或者__repr__
print(a)  # x,y,z
```

# 3.深入类和对象
鸭子类型就是多态的体现，是python的特性之一。在Java等静态语言中实现多态，需要继承父类并重写方法。而python的鸭子类型，具体来讲就是不同的类都实现了同一个名称的方法，那么在调用这个方法的时候，可以把这些不同的类看作相同的对象。比如list可以extend一个可迭代对象，那么list就不仅仅可以extend另一个list，还可以extend一个tuple，set等待，只要类型是可迭代的，就可以被extend，这就是鸭子类型，看着像鸭子，那就可以当成鸭子🦆。

python和Java的变量存在着本质不同。Java变量是定义时申请的一块内存空间，是一个盒子；python变量本质上是一个指针，是一个便利贴。例如在`a=1`这句代码中，python的本质是先向内存申请一个int类型的空间来放置1，然后把a贴在对象1上面，所以再有a='2'时，就是把a贴在对象2上，而不是把2分配给a；对于Java来讲，则是把对象2放在了a这个盒子里面。

因此有
```
a=[1,2]
b=a
b.append(3)
a.append(4)
print(a)  # [1,2,3,4]
```
这就是便利贴的体现，b贴在了a上面，而a贴在了对象`[1,2]`上面，所以a和b其实都是指向了同一个对象，即`a is b`是True。

**关于==和is的区别**
`==`比较的是值，而`is`比较的是id()，另外对于小整数和短字符串，python内部有驻留机制，保存在内存中，每次申请都是同一个对象。

**python的自省机制**
所谓的python自省机制，指的就是通过一定的机制查询到对象内部结构。对于__dict__可以查询对象的内部属性，dir()则是列出对象的所有属性名称。

**python的多重继承**
首先不推荐使用多重继承，这会导致复杂情况。python的多重继承按照MRO方法解析顺序，从左到右，新式类广度优先。super()调用的时候，从左到右，继承的同级间只执行左。
```
class A:
    def __init__(self):
        print('enter A')
        print('leave A')

class B:
    def __init__(self):
        print('enter B')
        print('leave B')

class C(B):
    def __init__(self):
        print('enter C')
        super().__init__()
        print('leave C')

class D(B,A):
    def __init__(self):
        print('enter D')
        super().__init__()
        print('leave D')

class E(C,D):
    def __init__(self):
        print('enter E')
        super().__init__()
        print('leave E')

class F(C):
    def __init__(self):
        print('enter F')
        super().__init__()
        print('leave F')

print(B())
print(C())
print(C.mro())
print(D())
print(D.mro())
print(E())
print(E.mro())
print(F())
print(F.__mro__)

# enter B
# leave B
# <__main__.B object at 0x1079cd7b8>
# enter C
# enter B
# leave B
# leave C
# <__main__.C object at 0x1079cd7b8>
# [<class '__main__.C'>, <class '__main__.B'>, <class 'object'>]
# enter D
# enter B
# leave B
# leave D
# <__main__.D object at 0x1079cd7b8>
# [<class '__main__.D'>, <class '__main__.B'>, <class '__main__.A'>, <class 'object'>]
# enter E
# enter C
# enter D
# enter B
# leave B
# leave D
# leave C
# leave E
# <__main__.E object at 0x1079cd7b8>
# [<class '__main__.E'>, <class '__main__.C'>, <class '__main__.D'>, <class '__main__.B'>, <class '__main__.A'>, <class 'object'>]
# enter F
# enter C
# enter B
# leave B
# leave C
# leave F
# <__main__.F object at 0x1079cd7b8>
# (<class '__main__.F'>, <class '__main__.C'>, <class '__main__.B'>, <class 'object'>)

```

# 4.python元类编程
@property动态属性，可以把方法调用改变成属性调用。

`__getattr__`是属性访问的出口，在找不到对象属性的时候，会进入此方法，可以在此添加一些灵活的逻辑。

`__getattribute__`是属性访问的入口，找对象属性会首先进入此方法，一般不能重写。

属性描述符：一个类中实现了`__get__`,`__set__`,`__delete__`三个魔法方法中的任意一个，都是属性描述符。通过属性描述符，可以对传入的属性值进行一系列的类型检查和范围检查等。

比如定义User类的age字段，需要是一个IntField()类型，那么IntField就是一个属性描述符。

**关于__new__和__init__的区别**
实例化一个类时，先调用__new__方法，再调用__init__方法，如果new不返回类对象，则不会调用init方法，即new是控制类生成的魔法方法。
```
class Us:
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, *args, **kwargs):
        pass

```

**关于type动态创建类**
```
def say(self):
    '''传递给动态创建类的方法'''
    return 'hello'
class BaseClass:
    '''传递给动态创建类的父类'''
    def answer(self):
        return 'this is baseclass'
User = type('User',(BaseClass,),{'name':'abc', 'say':say})
user = User()
print(user.name)  # abc
print(user.say())  # hello
print(user.answer())  # this is baseclass

```

python中类的实例化过程，会首先寻找metaclass，通过metaclass来创建User类；如果找不到，就去父类中找metaclass，还没有找到就去模块中找，都找不到，才会使用type创建类。

元类就是创建类的类，元类编程可以深度定制需求，增强代码健壮性，一般是高级编程使用，比如写一个框架。
```
class MetaClass(type):
    pass
class User(metaclass=MetaClass):
    pass

```

# 5.python多线程与多进程编程
由于GIL锁的存在，python中同一时刻只有一个线程运行在一个cpu上，不能多个线程映射到多个cpu上。GIL会在遇到IO操作或者执行一定时间片后主动释放。

对于IO操作来说，多线程和多进程性能差别不大，可能还会由于多进程的资源开销大导致性能反而更低
```
thread.start()  # 开启线程
thread.setDaemon(True)  # 设置守护线程，主线程运行完毕后kill掉当前线程
thread.join()  # 设置线程等待，主线程等待当前线程执行完毕之后再退出
```

线程间通信方式：共享变量，队列
