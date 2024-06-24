# Project_1/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
]


'''
path('admin/', admin.site.urls)
1.輸入http://127.0.0.1:8000/admin/可以進到後台做編輯

---

path('', include('myapp.urls'))
1.path('', ...) 中的空字符串 '' 表示根路径，即网站的根 URL（例如 http://127.0.0.1:8000/）。
2.当用户访问根 URL 时，这个路径会被匹配。

1.include('myapp.urls') 告诉 Django 在匹配到这个路径时，应包含 myapp 应用的 URL 配置。
2.也就是说，Django 会去加载 myapp/urls.py 文件，并根据其中定义的 URL 模式继续处理请求。

'''
