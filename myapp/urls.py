from django.urls import path
from .views import home, gym_data_api

urlpatterns = [
    path('', home, name = 'home'),
    path('api/gym-data/', gym_data_api, name = 'gym_data_api'),
]


'''
from .views import home, gym_data_api
->從當前目錄下找到views.py，匯入函式home, gym_data_api

path('', home, name = 'home')
->
1.其中path('', ...) 中的空字符串 '' 表示根路径，即网站的根 URL（例如 http://127.0.0.1:8000/）。
2.当用户访问根 URL 时，这个路径会被匹配。

path('api/gym-data/', gym_data_api, name = 'gym_data_api')
->
1.'api/gym-data/':單純一個名子的設定，用在網址，EX:http://127.0.0.1:8000/api/gym-data/
2. gym_data_api:從views.py裡面抓gym_data_api這個函式
3.name = 'gym_data_api'，寫這段之後就可以在其他地方使用，EX:home.html

'''
