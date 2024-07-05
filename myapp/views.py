
# views.py

from django.shortcuts import render #將一個模板和數據組合在一起，生成一個渲染後的 HTML 響應，然後將該響應返回給用戶端。
from django.http import JsonResponse  #Django 框架中导入 JsonResponse 类的语句。它用于在 Django 视图中创建和返回 JSON 响应
from .data_scraper_gym import scrape_data
from .data_scraper_buy_pchome import search_pchome_product as scrape_pchome_product
from .data_scraper_buy_momo import search_momo_product as scrape_momo_product

def home(request):  #当用户第一次访问网站时，Django 会调用这个视图。
    gym_data = scrape_data()
    return render(request, 'home.html', {'gym_data': gym_data})
   

def gym_data_api(request):  #用于提供动态数据更新的 API 端点。
    gym_data = scrape_data()
    return JsonResponse({'gym_data': gym_data})


def index(request):
    return render(request, 'index.html')


def buy_page(request):  # 更新視圖處理函數名稱
    return render(request, 'buy.html')


def search_form_pchome(request):
    return render(request, 'search_form_pchome.html')


def search_pchome_product_view(request):
    #request : HTTP 请求的所有信息，在目前情況下進到http://127.0.0.1:8000/search-form-pchome/這個網頁，輸入要搜尋的名稱，這樣就算是一種request (?
    if request.method == 'POST':
        #用来检查当前 HTTP 请求的方法是否为 POST，參考下方HTTP 请求方法
        product_name = request.POST.get('product_name')
        #product_name 是從 <label for="product_name">請輸入要搜索的商品名稱：</label> 輸入得到
        #.get('product_name') 方法用于从 request.POST 字典中获取键为 product_name 的值。
        results = scrape_pchome_product(product_name)
        #调用 scrape_pchome_product 的函数，并将 product_name 作为参数传递给该函数。
        return render(request, 'search_results_pchome.html', {'results': results})
        #簡單來說results的結果會套用到search_results_pchome.html裡面
    return render(request, 'search_form_pchome.html')
    #一開始一定會先進到這條，因為if request.method == 'POST'拿不到值，等到User輸入搜尋的商品


def search_form_momo(request):
    return render(request, 'search_form_momo.html')


def search_momo_product_view(request):
    #request : HTTP 请求的所有信息，在目前情況下進到http://127.0.0.1:8000/search-form-pchome/這個網頁，輸入要搜尋的名稱，這樣就算是一種request (?
    if request.method == 'POST':
        #用来检查当前 HTTP 请求的方法是否为 POST，參考下方HTTP 请求方法
        product_name = request.POST.get('product_name')
        #product_name 是從 <label for="product_name">請輸入要搜索的商品名稱：</label> 輸入得到
        #.get('product_name') 方法用于从 request.POST 字典中获取键为 product_name 的值。
        results = scrape_momo_product(product_name)
        #调用 scrape_pchome_product 的函数，并将 product_name 作为参数传递给该函数。
        return render(request, 'search_results_momo.html', {'results': results})
        #簡單來說results的結果會套用到search_results_pchome.html裡面
    return render(request, 'search_form_momo.html')
    #一開始一定會先進到這條，因為if request.method == 'POST'拿不到值，等到User輸入搜尋的商品


def search_form(request):
    return render(request, 'search_form_all.html')

def search_products(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')

        pchome_results = scrape_pchome_product(product_name)
        momo_results = scrape_momo_product(product_name)

        return render(request, 'search_results.html', {
            'pchome_results': pchome_results,
            'momo_results': momo_results
        })
    return render(request, 'search_form_all.html')





'''.
python manage.py runserver


HTTP 请求方法:
GET：用于请求数据，例如访问一个网页。数据通常通过 URL 查询参数传递。
POST：用于提交数据，例如提交一个表单。数据通常在请求体中传递。
PUT：用于更新数据。
DELETE：用于删除数据。


request.POST：
request.POST 是一个 QueryDict 对象，它类似于 Python 的字典，包含了所有通过 POST 请求提交的表单数据。
每个表单字段的名称作为键，字段的值作为相应的值存储在这个字典状对象中。













'''
