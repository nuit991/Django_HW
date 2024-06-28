from django.urls import path
from .views import home, gym_data_api, index

urlpatterns = [
    path('', index, name = 'index'),  # 這個是你的首頁,
    path('gym-page/', home, name='gym_page'),
    path('api/gym-data/', gym_data_api, name = 'gym_data_api'),
    
]



'''
from .views import home, gym_data_api
->從當前目錄下找到views.py，匯入函式home, gym_data_api
---

path('', home, name = 'home')
->
1.其中path('', ...) 中的空字符串 '' 表示根路径，即网站的根 URL（例如 http://127.0.0.1:8000/）。
2.当用户访问根 URL 时，这个路径会被匹配。
---

path('api/gym-data/', gym_data_api, name = 'gym_data_api')
->
1.'api/gym-data/':單純一個名子的設定，用在網址，EX:http://127.0.0.1:8000/api/gym-data/
2. gym_data_api:從views.py裡面抓gym_data_api這個函式
3.name = 'gym_data_api'，寫這段之後就可以在其他地方使用，EX:home.html
---

path('gym-page/', home, name='gym_page')
1.'gym-page/': 這是 URL 路徑部分。當用戶訪問 http://127.0.0.1:8000/gym-page/ 時，Django 會將這個請求映射到對應的視圖函數。這裡的 'gym-page/' 表示的是具體的 URL 路徑部分。
2.home: 是與 URL 路徑相關聯的視圖函數。當用戶訪問 'gym-page/' 時，Django 會調用 views.py 中的 home 函數來處理該請求。
3.name='gym_page': 這是路徑名稱，用於在 Django 應用中引用這個 URL 路徑。路徑名稱允許你在模板或其他地方使用 url 模板標籤來生成這個 URL。例如，在 index.html 模板中，按鈕的 onclick 屬性中使用了 {% url 'gym_page' %}，這將生成 /gym-page/ 的 URL。


'''
