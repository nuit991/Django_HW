#import asyncio: 导入 asyncio 模块，它是 Python 的标准库，用于编写异步代码，尤其是处理协程、事件循环等。
import asyncio
#import json: 导入 json 模块，用于处理 JSON 数据的序列化和反序列化（即将 Python 对象转换为 JSON 字符串，以及从 JSON 字符串中恢复 Python 对象）。
import json
#from channels.generic.websocket import AsyncWebsocketConsumer: 从 channels 库中导入 AsyncWebsocketConsumer 类。
#AsyncWebsocketConsumer 是 Django Channels 中的一个基类，用于创建处理 WebSocket 连接的消费者。它提供了处理 WebSocket 消息、连接和断开的异步方法。
#channels 註解寫在下面
from channels.generic.websocket import AsyncWebsocketConsumer
from .data_scraper_buy_yahoo import search_yahoo_product as scrape_yahoo_product

#Momo_Consumer 继承自 AsyncWebsocketConsumer，这是 Django Channels 提供的一个类，用于处理 WebSocket 连接的异步操作。
class Yahoo_Consumer(AsyncWebsocketConsumer):
    #这是一个异步方法，用于处理 WebSocket 连接的建立。connect 方法会在 WebSocket 客户端尝试连接到服务器时被调用。
    async def connect(self):
        #设置实例属性 channel_name，用于标识这个 WebSocket 连接所属的频道。在这个例子中，channel_name 被设置为 'momo_channel'。这个属性可以用来管理和区分不同的 WebSocket 连接或频道。
        self.channel_name = 'yahoo_channel'
        #这行代码会在服务器端的控制台输出 'momo_channel'。这是一个调试输出，帮助开发人员确认 connect 方法被调用时的状态。实际开发中，这个输出可以帮助你验证 WebSocket 连接是否成功建立。
        print('yahoo_channel')
        #await 关键字表示这是一个异步操作。self.accept() 是一个异步方法，用于接受 WebSocket 连接。调用这个方法会发送一个响应给客户端，确认 WebSocket 连接已经被接受并可以开始进行数据通信。
        #只有在调用了 accept() 方法后，客户端才能向服务器发送数据。
        await self.accept()  # 接受 WebSocket 连接


    #disconnect 是 WebSocket 消费者的一个异步方法，当 WebSocket 连接关闭时会被调用。它的参数 close_code 是一个整数，表示关闭连接的原因代码（例如，正常关闭、协议错误等）。
    async def disconnect(self, close_code):
        #hasattr 函数用于检查对象 self 是否具有指定的属性(白話一點就是這樣self.product_task)。在这里，hasattr(self, 'product_task') 检查 self 对象是否有名为 product_task 的属性。
        #self.product_task 是之前在消费者中创建的异步任务的引用，通常是在 connect 方法中创建的任务。
        if hasattr(self, 'product_task'):
            #如果 self 对象有 product_task 属性（即 self.product_task 存在），self.product_task.cancel() 会被调用以取消该任务。
            #cancel() 方法用于请求取消异步任务。这并不会立即终止任务，而是向任务发送取消请求。任务会在下一个检查点检查取消请求，并在适当的时候停止执行。
            self.product_task.cancel()



    #流程: 接收数据 -> 解析数据 -> 创建并调度异步任务。
    #用于处理 WebSocket 客户端发送到服务器的消息。
    async def receive(self, text_data):  #text_data->前端丟的數據，這邊就是指product_name / max_pages
        #打印接收到的消息。这有助于调试，查看从客户端接收到的数据是什么。
        print(f"Yahoo_Received data: {text_data}")
        #将接收到的 JSON 字符串转换为 Python 字典。json.loads 函数用于解析 JSON 字符串并返回相应的字典对象。
        data = json.loads(text_data)
        #从解析后的字典中获取 product_name 的值。data.get 方法用于获取字典中的值，如果键不存在，则返回 None。
        product_name = data.get('product_name_yahoo')
        #从字典中获取 max_pages 的值，并将其转换为整数。data.get('max_pages', 5) 意味着，如果 max_pages 键不存在，则默认值为 5。int 函数将其转换为整数类型。
        max_pages = int(data.get('yahoo_max_pages', 5))
        #使用 asyncio.create_task 创建一个新的异步任务，调用 self.send_product_data 方法。
        #asyncio.create_task 用于调度异步任务，self.product_task 保存了这个任务对象，以便后续可以取消或检查任务的状态。
        self.product_task = asyncio.create_task(self.send_product_data(product_name, max_pages))



    #定义一个异步方法 send_product_data，用于处理产品数据的发送。
    async def send_product_data(self, product_name, max_pages):
        print("Yahoo_send_product_data called")
        #使用异步 for 循环从 scrape_momo_product 函数获取产品数据。
        async for prd_name, product_url, price, img_url in scrape_yahoo_product(product_name, max_pages): 
            data = {
                'prd_name': prd_name,
                'product_url': product_url,
                'price': price,
                'img_url': img_url
            }
            print('Yahoo___Sending data:', data) 
            #通过 WebSocket 发送数据给客户端。
            #json.dumps(data) 将数据字典转换为 JSON 格式的字符串，self.send() 是 WebSocket 消费者提供的方法，用于发送消息。
            await self.send(text_data=json.dumps(data)) 
            await asyncio.sleep(1)  # 延迟，避免发送过快
        #20240816
        #告诉前端数据抓取已经完成
        print("Sending completion status")
        await self.send(text_data=json.dumps({'status': 'completed'}))



'''

什么时候需要 receive?
如果你的需求变更，比如希望客户端发送一个命令来触发图像推送，或发送参数来改变推送行为，那么就会需要定义 receive 方法。
EX_1:
在这个例子中，客户端发送 "command": "start"，然后服务器才开始推送图像。这样就需要 receive 方法来处理这个命令。

EX_2:
上面的async def receive(self, text_data):
因為前端有丟給後台product_name / max_pages所以要用receive




channels 註解

1.要先安裝
pip install channels

2.檢查
pip show channels

3.前往settings.py，這東西在Project_1
新增這些
INSTALLED_APPS = [
    # ... 你的其他应用
    'channels',
]
ASGI_APPLICATION = 'Project_1.asgi.application'

4.创建 ASGI 配置，新增asgi.py，也是在Project_1下面


'''