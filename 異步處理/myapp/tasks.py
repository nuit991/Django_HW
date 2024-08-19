'''
#asyncio: Python 的异步 I/O 模块，用于处理异步任务。
import asyncio
#get_channel_layer 是 Django Channels 提供的一个函数，用于获取频道层（channel layer）。频道层是 Django Channels 中的核心组件，用于处理 WebSocket 连接和消息传递。
from channels.layers import get_channel_layer
#async_to_sync 是 asgiref 包中的一个工具函数，用于将异步代码转换为同步代码。asgiref 是 Django 用于处理 ASGI（Asynchronous Server Gateway Interface）兼容的库。
#註解在下面
from asgiref.sync import async_to_sync
from .data_scraper_buy_momo import search_momo_product
#json 是 Python 标准库中的一个模块，用于处理 JSON 数据。JSON（JavaScript Object Notation）是一种轻量级的数据交换格式，易于人类阅读和编写，也易于机器解析和生成
#在 Python 中将数据编码为 JSON 格式（json.dumps），或将 JSON 数据解码为 Python 对象（json.loads）。在 WebSocket 通信中，通常会使用 JSON 格式来传输数据。
import json

def start_websocket_task(product_name, max_pages):
    """
    启动 WebSocket 任务来抓取数据并通过 WebSocket 发送数据。
    """
    #async def run_task(): 这是一个异步函数，使用 async def 关键字定义，表示函数内部可以使用 await 关键字来等待异步操作。
    async def run_task():
        #channel_layer = get_channel_layer(): 获取 Django Channels 的 channel_layer，用于发送和接收 WebSocket 消息。
        #註解在下面
        channel_layer = get_channel_layer()
        channel_name = 'momo_channel'  # 选择一个合适的频道名称

        async for prd_name, product_url, price, img_url in search_momo_product(product_name, max_pages):
            data = {
                'prd_name': prd_name,
                'product_url': product_url,
                'price': price,
                'img_url': img_url
            }
            #await channel_layer.send(...): 使用 await 关键字异步地通过 WebSocket 频道发送数据。
            #channel_layer.send(): 发送数据到指定的频道（channel_name），channel_name 是 'momo_channel'，这个名称应该和消费者中的频道名称匹配。
            await channel_layer.send(
                channel_name,
                {   #type: 指定消息类型为 'websocket.send'，这是 Django Channels 中的一个标准消息类型，用于发送 WebSocket 消息。
                    #會把資料丟到 consumers_momo.py
                    'type': 'websocket.send', 
                    #text: 发送的消息内容，使用 json.dumps(data) 将字典格式的数据转换为 JSON 字符串。
                    'text': json.dumps(data) 
                }
            )
            await asyncio.sleep(0.5)  # 延迟以避免发送过快

    #async_to_sync(run_task): 将异步函数 run_task 转换为同步函数。这是因为在某些同步上下文（如 Django 的视图函数）中，不能直接运行异步代码。
    #()：调用转换后的同步函数以实际运行任务。
    async_to_sync(run_task)()


async_to_sync 是 asgiref 库中的一个工具函数，用于将异步代码转换为同步代码。
主要作用是将异步操作（async 函数）包装成同步操作，以便在传统的同步上下文中执行。

--------
asyncio 跟 asgiref.sync 差別

asyncio:
是 Python 标准库的一部分，用于原生的异步编程。
提供事件循环、协程、异步 I/O 等功能。

asgiref.sync:
是 asgiref 库中的一部分，主要用于在异步和同步环境之间转换代码。
提供 async_to_sync 和 sync_to_async 工具，以便在不同编程模型中互操作。
asyncio 专注于创建和管理异步操作，而 asgiref.sync 主要处理同步和异步代码之间的兼容性问题。

--------
channel_layer = get_channel_layer()

1.channel_layer 是一个用于处理和发送 WebSocket 消息的核心组件。
channel_layer 的获取方式和配置步骤如下：
在Project_1/settings.py，其中CHANNEL_LAYERS = {...}

2. 获取 channel_layer
获取 channel_layer 的方法是通过 Django Channels 提供的 get_channel_layer() 函数。
这个函数会根据 CHANNEL_LAYERS(在Project_1/settings.py) 配置返回一个 channel_layer 实例。

3. 使用 channel_layer
一旦你获取了 channel_layer，你可以使用它来发送和接收消息。
接收消息通常在消费者中处理。你可以在消费者的 receive 方法中处理接收到的消息

總結:
配置 CHANNEL_LAYERS: 在 settings.py 中配置 CHANNEL_LAYERS，指定后端和相关参数。
获取 channel_layer: 使用 get_channel_layer() 函数来获取 channel_layer 实例。
使用 channel_layer: 使用 channel_layer 实例来发送和接收消息。



'''