"""import  asyncio

@asyncio.coroutine
def hello():
    print("Hello world")
    # 异步调用asyncio.sleep(1):
    r = yield  from asyncio.sleep(1)
    print("hello again")

# 获取EventLoop:
loop = asyncio.get_event_loop()
# 执行coroutine
loop.run_until_complete(hello())
loop.close()
"""

"""
import threading
import asyncio

@asyncio.coroutine
def hello():
    print("Hello world! (%s)"% threading.current_thread())
    yield from asyncio.sleep(1)
    print('Hello again! (%s)' % threading.currentThread())

loop = asyncio.get_event_loop()
tasks = [hello(),hello()]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
"""
"""
import asyncio

@asyncio.coroutine
def wget(host):
    print("wget:%s ..."%host)
    connect = asyncio.open_connection(host,80)
    reader,writer = yield from connect
    header = "GET / HTTP/1.0\r\nHost: %s\r\n\r\n" %host
    writer.write(header.encode("utf-8"))
    yield from writer.drain()
    while True:
        line = yield  from reader.readline()
        if line == b"\r\n":
            break
        print('%s header > %s' %(host,line.decode("utf-8").rstrip()) )
    writer.close()

loop = asyncio.get_event_loop()
tasks = [wget(host) for host in ['www.sina.com.cn', 'www.sohu.com', 'www.163.com']]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
"""
"""
import asyncio

from aiohttp import web

async def index(request):
       await asyncio.sleep(0.5)
       return web.Response(body=b"<h1>Index</h1>")

async  def hello(request):
       await asyncio.sleep(0.5)
       text = "<h1>hello, %s!</h1>"% request.math_info["name"]
       return web.Response(body=text.encode('utf-8'))

async def init(loop):
       app = web.Application(loop= loop)
       app.router.add_route("GET","/",index)
       app.router.add_route("GET","/hello/{name}",hello)
       srv = await loop.create_server(app.make_handler(),"127.0.0.1",8000)
       print('Server started at http://127.0.0.1:8000...')
       return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()
"""
class Student(object):
       pass


class ListMetaclass(type):
       # cls 当前准备创建的类的对象
       #name；l类的名字
       #bases 类继承的父类集合
       #attrs 类的方法集合
       def __new__(cls,name,bases,attrs):
              attrs["add"] = lambda self,value:self.append(value)
              return type.__new__(cls,name,bases,attrs)

class Mylist(list,metaclass=ListMetaclass):
       pass

L = Mylist()
L.add(1)
print(L)