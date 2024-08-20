#这行代码导入了 re_path 函数，它允许使用正则表达式来定义 URL 模式。
#re_path 是 Django 的 URL 解析器之一，可以更灵活地匹配复杂的 URL 模式。
from django.urls import re_path
#. (dot) 代表当前包或模块所在的目录。
#假設在A Folder下面就要用 from .A
from . import consumers, consumers_momo, consumers_pchome, consumers_yahoo
#这是一个列表，用于存放 WebSocket URL 的路由配置。这个列表会在 Django 的 ASGI 配置中被引用，以确定哪些 URL 应该由哪些 WebSocket 消费者处理。
websocket_urlpatterns = [
    #这个 URL 模式使用了 re_path 函数，并定义了一个 WebSocket 路由。
    #r'ws/counter/': 这是一个原始字符串（原始字符串以 r 开头），它定义了匹配的 URL 模式。在这个例子中，ws/counter/ 是 WebSocket 连接的路径
    #如果客户端连接到 ws://yourdomain/ws/counter/，这个 URL 会被匹配。
    #consumers.CounterConsumer.as_asgi(): 这是一个 WebSocket 消费者类，CounterConsumer 通过 as_asgi() 方法被转换为一个 ASGI 应用，以处理 WebSocket 请求。
    #CounterConsumer 类负责处理在 ws/counter/ 路径上收到的所有 WebSocket 请求。 (會去找consumsers.py)
    re_path(r'ws/counter/', consumers.CounterConsumer.as_asgi()),
    re_path(r'ws/momo/', consumers_momo.Momo_Consumer.as_asgi()),
    re_path(r'ws/pchome/', consumers_pchome.Pchome_Consumer.as_asgi()),
    re_path(r'ws/yahoo/', consumers_yahoo.Yahoo_Consumer.as_asgi()),

]
