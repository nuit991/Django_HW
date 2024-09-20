# myproject/asgi.py
import os
# 从 Django 中导入 get_asgi_application 函数。这个函数为 Django 项目提供了一个标准的 ASGI 应用接口，类似于 WSGI 接口，但支持异步。
from django.core.asgi import get_asgi_application
# 从 channels.auth 导入 AuthMiddlewareStack。AuthMiddlewareStack 是一个 Channels 提供的中间件，它允许在 WebSocket 连接中使用 Django 的身份验证系统。
# 这确保了 WebSocket 连接与 Django 中的用户会话保持一致，像 Django 的登录机制一样，能识别用户身份。
from channels.auth import AuthMiddlewareStack
# ProtocolTypeRouter 是 Channels 用来根据请求类型（HTTP、WebSocket 等）选择处理方式的路由器。
# 它允许你为不同的协议类型（如 HTTP 或 WebSocket）定义不同的处理程序。
# URLRouter 是用来根据 URL 路径来路由 WebSocket 连接的路由器，类似于 Django 的 URL 路由机制。
from channels.routing import ProtocolTypeRouter, URLRouter
from myapp import routing

# 这行代码的目的是告诉 Django 应用程序应该加载 Project_1 项目的 settings.py 配置文件。它是 Django 启动时的关键步骤，确保项目运行时能加载正确的设置。
# 這一段告诉 Django 去加载这些配置，使得 Django 知道如何启动项目、连接数据库、加载应用、处理静态文件等。
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project_1.settings')

# ProtocolTypeRouter 是 Channels 提供的一个路由器，它根据连接协议的不同，分发不同类型的请求。它可以处理多种协议，例如 HTTP 和 WebSocket。
application = ProtocolTypeRouter({
    # 这一行处理普通的 HTTP 请求。get_asgi_application() 是 Django 提供的一个函数，它返回标准的 ASGI 应用，专门处理 HTTP 请求。
    "http": get_asgi_application(),
    # 一行处理 WebSocket 请求。AuthMiddlewareStack 是 Channels 提供的一个中间件，用来为 WebSocket 连接提供用户认证（类似于 HTTP 请求中的认证系统）。
    # 它会确保用户认证信息能够通过 WebSocket 传递，从而让你在 WebSocket 连接中也能访问认证用户。
    "websocket": AuthMiddlewareStack(
        #URLRouter 是 Channels 的路由系统，用来处理 WebSocket 请求。它会根据 WebSocket URL 模式，把请求分发给对应的处理程序。
        URLRouter(
            #routing.websocket_urlpatterns 是你在 myapp/routing.py 文件中定义的 WebSocket URL 模式。这部分定义了哪些 WebSocket URL 会被接受以及如何处理这些连接。
            routing.websocket_urlpatterns
        )
    ),
})



'''
代码片段总结
这个代码片段的目的是创建一个 ASGI 应用，并且支持 WebSocket 和 HTTP 协议的处理。
它将 HTTP 请求交给 Django 自带的 ASGI 处理程序（get_asgi_application），将 WebSocket 请求通过 URLRouter 路由给 Channels，处理 WebSocket 连接时的身份验证通过 AuthMiddlewareStack 完成。

-------------
os.environ
os.environ 是 Python 中的一个字典对象，它包含了操作系统环境变量的键值对。
可以通过 os.environ 读取和设置环境变量，这些变量用于配置应用程序的运行环境。

-------------
setdefault()
setdefault 是字典的方法。它的作用是：
如果字典中已经存在该键，则返回对应的值。
如果字典中不存在该键，则将该键的值设置为指定的默认值，并返回该值。
在这里，setdefault 确保 DJANGO_SETTINGS_MODULE 环境变量已经被设置。如果该变量不存在，则设置为 'Project_1.settings'。

-------------
'DJANGO_SETTINGS_MODULE'
这是 Django 识别项目配置文件的环境变量名称。
Django 使用这个环境变量来确定应该加载哪个配置文件，通常是 settings.py。

-------------
Project_1.settings'
'Project_1.settings' 是项目的配置模块路径。
Project_1 是 Django 项目的名称，settings 是 Django 的设置文件，用于配置项目的数据库、应用、静态文件等。
这行代码告诉 Django 在启动时使用 Project_1 项目中的 settings.py 文件作为配置文件。

'''