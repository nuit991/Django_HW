"""
URL configuration for Project_1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# Project_1/urls.py

#这是导入 Django 自带的管理模块，用于启用 Django 管理后台。
from django.contrib import admin

#path：Django 中的 URL 路由方法，用于将某个特定 URL 路径与一个视图函数或包含文件关联起来。
#include：允许你将其他 URL 配置文件包含进来，便于管理不同应用的 URL 路由，尤其当项目变大时。
from django.urls import path, include

urlpatterns = [
    #当用户访问 http://yourdomain.com/admin/ 时，Django 会将请求交给 admin.site.urls 处理。
    #admin.site.urls 是 Django 内置的管理后台的 URL 配置，通常用来访问 Django 管理后台界面。
    path('admin/', admin.site.urls),
    #这里的 path('', ...) 表示当用户访问网站根路径（如 http://yourdomain.com/）时，Django 将请求交给 myapp.urls 处理。
    #include('myapp.urls') 会将请求路由到 myapp 应用中的 urls.py 文件中去寻找更多的 URL 路由定义。这种方式使得你可以在不同的 Django 应用中各自管理自己的 URL 路由，保持项目的可维护性。
    path('', include('myapp.urls')),
]


'''

網頁上輸入127.0.0.1，會先到這邊詢問path('', include('myapp.urls'))，然後這邊再去myapp/urls.py裡面詢問

'''