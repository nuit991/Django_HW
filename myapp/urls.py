from django.urls import path
from .views import home, gym_data_api, index, buy_page, search_pchome_product_view, search_form_pchome

urlpatterns = [
    path('', index, name = 'index'),  # 這個是你的首頁,
    path('gym-page/', home, name = 'gym_page'),
    path('buy-page/', buy_page, name='buy_page'),
    path('api/gym-data/', gym_data_api, name = 'gym_data_api'),

    path('search-form-pchome/', search_form_pchome, name='search_form_pchome'),
    path('search-pchome-product/', search_pchome_product_view, name='search_pchome_product'),
    
]






'''
from django.urls import path
from .views import home #表示当前目录下的 views.py 文件，home 是在 views.py 文件中定义的视图函数的名称。

urlpatterns = [
    path('', home, name='home'),
]
'''


'''
1.''：这个空字符串表示根路径，即网站的根 URL（例如 http://example.com/）
2.home：这是路由到的视图函数，即当用户访问根路径时，会调用名为 home 的视图函数处理请求。
3.name='home'：这是路由的名称，可以在 Django 的其他地方通过这个名称来引用这个路由，例如在模板中使用 {% url 'home' %} 获取这个路由的 URL。

'''
