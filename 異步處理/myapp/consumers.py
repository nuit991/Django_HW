import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .AI import scrape_images as scrape_images  #要用的函數記得匯入

class CounterConsumer(AsyncWebsocketConsumer):
    async def connect(self): #当客户端建立 WebSocket 连接时调用此方法。
        await self.accept() #接受 WebSocket 连接，使其处于打开状态，以便进行通信。
        self.image_task = asyncio.create_task(self.send_images()) #创建一个异步任务 self.image_task，该任务会调用 send_images 方法来发送图像。 

    async def disconnect(self, close_code): #当 WebSocket 连接断开时调用此方法。
        if hasattr(self, 'image_task'): #检查 self 对象是否具有 image_task 属性，以确保任务存在。
            self.image_task.cancel() #如果任务存在，则取消正在进行的 image_task 任务，防止在连接关闭后继续执行不必要的任务。

    async def send_images(self): #如果任务存在，则取消正在进行的 image_task 任务，防止在连接关闭后继续执行不必要的任务。
        print("ru OKOKOKO")
        async for img_url in scrape_images(): #异步循环，通过 scrape_images 函数逐个获取图像 URL。
            await self.send(text_data=json.dumps({'img_url': img_url})) #通过 WebSocket 发送获取到的图像 URL，数据以 JSON 格式封装后发送。
            await asyncio.sleep(0.5)  # 可选的延迟，避免发送过快




'''


這邊改完要重新啟動 daphne
要注意設定9000，不能跟django的port號一樣
daphne -p 9000 Project_1.asgi:application





'''