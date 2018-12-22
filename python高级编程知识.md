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
thread.setDaemon(True)  # 设置守护线程，主线程运行完毕后kill掉当前线程，需要在start()前调用
thread.join()  # 设置线程等待，主线程等待当前线程执行完毕之后再退出
```

线程间通信方式：共享变量，队列。共享变量的方式，线程不安全，需要加锁。queue.Queue队列是线程安全的双端队列，本质上采用deque

进程间通信的方式：multiprocessing.Queue，pipe(2个进程间通信), 内存共享Manager。进程间不能采用共享变量的方式来通信，而multiprocessing的Queue不能用于进程池Pool，Pool中的进程间通信需要使用manager中的Queue。线程池和进程池，需要pool.close()，再pool.join()。
```
from queue import Queue            # 线程间用
from multiprocessing import Queue  # 进程间用
from multiprocessing import Manager 
Manager().Queue()                  # 进程池用

```
管道pipe只能用于2个进程间通信，一个pipe.send(),一个pipe.recv()

**线程同步**

对于`a += 1`这一语句，从字节码的层面看有4步，这中间可能会产生线程切换，导致错误：
1. load a
2. load 1
3. 执行+
4. 赋值给a

线程同步，可以采用锁，但是锁会影响性能，还可能导致死锁。锁有2种，Lock和RLock(可重入的锁)，在同一线程中，Lock只能一次acquire()接着一次release(),如果连续两次acquire就会死锁，RLock则可以在同一个线程中，多次acquire，只要和release相对应次数就可以。

还可以采用condition，条件变量，用于复杂的线程同步(内部调用的还是RLock)。模型如下：
```
# 对于生产者：(如果不用with需要在前后加上acquire和release)
with cond:
    do_somethong()
    condition.notify()
    condition.wait()
# 对于消费者
with cond:
    condition.wait()
    do_somethong()
    condition.notify()
  
# 生产者通知消费者，需要消费者先处于wait()状态
```
启动线程的时候，消费者要先启动等待，生产者再启动，否则生产者的信号发出去了，消费者还没有启动，就无法接收到信号。

condition有2层锁，底层锁会在线程调用wait方法后释放，顶层锁会在调用wait的时候分配一把并放在condition的等待队列中，等待notify方法的唤醒。

Semaphore 信号量，是用于控制进入数量的锁(内部使用condition实现的)。在一个线程中acquire，在另一个线程中release，需要被传参

多线程可以使用threading库，ThreadPoolExecutor;多进程可以使用multiprocessing，ProcessPoolExecutor

# 6.协程与异步IO
* 并发(一个时间段内，多个程序在一个cpu上运行，任意时刻只有一个程序运行)
* 并行(任意时间点，多个程序在多个cpu上同时运行)
* 同步(代码调用IO操作时，必须等待IO操作完成才返回的调用方式)
* 异步(代码调用IO操作时，不必等IO操作完成就立即返回的调用方式)
* 阻塞(调用函数时，当前线程被挂起)
* 非阻塞(调用函数时，当前函数不会被挂起，而是立即返回)
* 同步/异步是消息通信的一种机制
* 阻塞/非阻塞是函数调用的一种机制

C10K问题：如何在1核1GHz的CPU，2G内存，1gbps网络环境下，让单台服务器同时为1万个客户端提供FTP服务

C10M问题：如何利用8核CPU，64G内存，在10gbps的网络上保持1000万并发连接

Unix下5中I/O模型：阻塞式，非阻塞式，I/O复用，信号驱动式，异步I/O。大多数异步框架使用的技术还是IO多路复用，因为技术更加成熟，而不是异步IO的aio。而很多异步IO的框架模型中，实际上采用的都是一种epoll+回调+事件循环的方式。

I/O多路复用：通过一种机制，一个进程可以监视多个FD文件描述符，一旦某个描述符就绪(一般是读写就绪)，就通知程序进行相应读写操作。

三种技术：select，poll，epoll，本质上都是同步I/O，因为他们都需要在就绪后自己复杂读写，即自己既负责监听，又负责读写操作。所谓的读写操作，就是把数据从内核空间拷贝到用户空间，而异步I/O无需做这一步因为操作系统完成这个操作后才通知。
* select优点是良好的跨平台支持，缺点是虽然可以监听多个socket状态但是有数量限制，且需要全部轮询获取就绪的描述符
* poll解决了最大监听数量的限制，但是仍然需要轮询获取就绪描述符
* epoll更加灵活，没有描述符限制，但是不支持win平台

epoll并不比select就好。在高并发，连接活跃度不高的情况下，epoll更好。但是在并发不高，连接活跃的情况下，select更好。

**协程**

可以暂停并恢复的函数，且可以向暂停的对方传值。主要是为了解决如下问题：
1. 回调模式编写代码复杂度高
2. 同步编程的并发性不高
3. 多线程编程需要线程同步，lock影响性能 

所以协程具有以下功能：
1. 采用同步方式去编写异步的代码
2. 采用单线程去切换任务

使用单线程意味着我们需要自己调度任务，而不是操作系统自动切换。单线程不需要锁，并发性高，线程内切换函数性能远高于线程间切换

利用生成器来完成协程，生成器不只可以产出值，还可以接收值。启动生成器有2种方式，next和send
```
# 基本生成器
def gen_func():
    yield 1
    yield 2
    return 'ok'
gen = gen_func()
print(next(gen))  # 1
print(next(gen))  # 2
print(next(gen))  # StopIteration: ok

# 可以传值的生成器
def gen_func2():
    # 对yield进行赋值时，1可以生成值，2可以接收值
    html = yield 'http;//www.baidu.com'
    print(html)  # hello yield
    yield 2
    return 'ok'
gen2 = gen_func2()
# 在调用send之前，需要启动一次生成器，且必须是gen2.send(None)，或者采用next(gen2)的方式
url = gen2.send(None)
# download url
html = 'hello yield'
# send方法可以传递值到生成器内部，同时还可以启动生成器执行到下一个yield位置
print(gen2.send(html))  # 2

```

**yield from iterable**

可以将可迭代序列里的值一个一个yield出来，不仅如此，yield from还可以建立调用方与子生成器的双向通道
```
# yield和yield from
def g1(iterable):
    yield iterable
def g2(iterable):
    yield from iterable

for value in g1(range(3)):
    print(value)  # range(0, 3)
for value in g2(range(3)):
    print(value)  # 0,1,2


# 委托生成器
def g1(gen):
    # gen是子生成器
    yield from gen  # yield from会在调用方main与子生成器gen之间建立一个双向通道
# 调用方
def main():
    g = g1()
    g.send(None)  # 预激

```

本来协程是采用生成器来实现的,旧版本可以使用@coroutine+yield实现协程，python为了将语义明确，3.5版本引入了async/await关键词用于定义原生协程
```
async def downloader(url):
    return 'ok'

async def down_url(url):
    html = await downloader(url)
    return html

coro = down_url('http://www.baidu.com')
coro.send(None)  # StopIteration: ok
```

# 7.asyncio并发编程
asyncio是python用于解决异步IO编程的一整套解决方案

* 包含各种特定系统实现的模块化事件循环
* 传输和协议抽象
* 基于yield from的协议和任务，可以让你用顺序的方式编写并发代码
* 当必须使用一个将产生阻塞IO的调用时，有接口可以把这个事件转移到线程池
* 模仿threading模块中的同步原语，可以用在单线程内的协程之间

并发编程三要素：事件循环+回调/驱动生成器+epoll(IO多路复用)
```
# 简单调用
import asyncio
async def get_html(url):
    print('start get url')
    await asyncio.sleep(2)
    print('end get url')

start_time = time.time()
loop = asyncio.get_event_loop()
tasks = [get_html('') for _ in range(5)]
loop.run_until_complete(asyncio.wait(tasks))
# loop.run_until_complete(asyncio.gather(*tasks))  # 与上句效果相同
print(time.time()-start_time)


# gather和wait的区别
# gather更加高级，可以进行分组，可以取消组任务
# group1 = ['','']
# group2 = ['','','']
# group1 = asyncio.gather(*group1)
# group2 = asyncio.gather(*group2)
# group2.cancel()
# loop.run_until_complete(asyncio.gather(group1,group2))
```

```
# future调用，获取返回值，添加callback
async def get_html(url):
    print('start get url')
    await asyncio.sleep(2)
    return 'hello asyncio'

# 用偏函数，指定的参数需要放在前面，future是调用传入的默认参数放在最后
def callback(url, future):
    print(url)
    print('have callback url')

start_time = time.time()
loop = asyncio.get_event_loop()
future = asyncio.ensure_future(get_html('myurl'))
# future = loop.create_task(get_html('myurl'))  # 与上面效果相同
# partial是一个偏函数，包装一个函数和参数，返回一个函数名
future.add_done_callback(partial(callback, 'myrul'))
loop.run_until_complete(future)
print(future.result())
print(time.time()-start_time)
# start get url
# myrul
# have callback url
# hello asyncio
# 2.0035648
```
`run_until_complete`和`run_forever`的区别：前者运行完会停止，后者会一直挂起。在run_forever中如何停止呢？因为loop会被传到future中，因此可以在future中close。这里loop设计是环状的，loop-future，不太好的设计方式。

```
# 取消task
loop = asyncio.get_event_loop()
tasks = []
try:
    loop.run_until_complete(asyncio.wait(tasks))
except KeyboardInterrupt as e:
    all_tasks = asyncio.Task.all_tasks()
    for task in all_tasks:
        task.cancel()
    # 下面是固定用法，stop后还需要run_forever，否则会报错
    loop.stop()
    loop.run_forever()
finally:
    loop.close()
```

**协程中嵌套协程**

loop中注册task，task调用协程，协程调用子协程，子协程直接返回数据给task，等到子协程执行完成后，抛出一个stop异常，被协程捕捉，然后协程同样抛出stop异常给task，然后task标记为done返回给loop。

asyncio的几个特殊方法：call_soon(),call_later(),call_at(),call_soon_threadsafe()

线程池ThreadPoolExecutor与asyncio相结合，在协程中集成阻塞IO。一般协程内不能拥有阻塞方法，否则会阻塞整个协程运行，但是某些情况下需要调用一些阻塞接口，这时就需要集成了。
```
import asyncio
from concurrent.futures import ThreadPoolExecutor
# 假设get_html是一个阻塞的方法
loop = asyncio.get_event_loop()
executor = ThreadPoolExecutor()
tasks = []
for i in range(20):
    url = 'http://book/{}'.format(i)
    task = loop.run_in_executor(executor, get_html, url)
    tasks.append(task)
loop.run_until_complete(asyncio.wait(tasks))
```

**asyncio同步和通信**

在asyncio中调用async函数时，如对一个共享变量分别进行加减操作，如果函数不yield或者await，那么由于是单线程的，所以协程不再需要锁，对共享变量的操作是符合预期的。但是如果函数中有yield或者await，那么可能会产生对同一个资源多次竞争调用的问题，所以还是需要Lock。这时采用的是asyncio的lock。如果不采用lock加锁，那么可以使用Queue(使用方式为await queue.get())。其实由于协程本质上还是单线程的原因，其同步和通信相比线程要简单
```
import asyncio
import aiohttp
from asyncio import Lock, Queue
cache={}
lock = Lock()

async def get_stuff(url):
    async with lock:
        if url in cache:
            return cache[url]
        stuff = await aiohttp.request('GET', url)
        cache[url] = stuff
        return stuff
# 两个方法都会调用get_stuff，可能会对同一个URL进行竞争调用
async def parse_stuff(url):
    stuff = await get_stuff(url)
async def user_stuff(url):
    stuff = await get_stuff(url)
```
