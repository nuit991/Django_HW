
# views.py

from django.shortcuts import render #將一個模板和數據組合在一起，生成一個渲染後的 HTML 響應，然後將該響應返回給用戶端。
from django.http import JsonResponse  #Django 框架中导入 JsonResponse 类的语句。它用于在 Django 视图中创建和返回 JSON 响应
#from .data_scraper_gym import scrape_data
from .data_scraper_buy_pchome import search_pchome_product as scrape_pchome_product
from .data_scraper_buy_momo import search_momo_product as scrape_momo_product
from .data_scraper_buy_yahoo import search_yahoo_product as scrape_yahoo_product
#from .AI import scrape_images as scrape_images
#from .tasks import start_websocket_task

#圖片處理
from django.core.paginator import Paginator
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Image
import os



def index(request):
    return render(request, 'index.html')

def search_form_pchome(request):
    return render(request, 'search_form_pchome.html')


def search_pchome_product_view(request):
    #request : HTTP 请求的所有信息，在目前情況下進到http://127.0.0.1:8000/search-form-pchome/這個網頁，輸入要搜尋的名稱，這樣就算是一種request (?
    if request.method == 'POST':
        print(request.POST)
        #用来检查当前 HTTP 请求的方法是否为 POST，參考下方HTTP 请求方法
        product_name_pchome = request.POST.get('product_name_pchome')
        print(product_name_pchome)
        pchome_max_pages = int(request.POST.get('pchome_max_pages', 5))
        print(pchome_max_pages)
        #product_name 是從 <label for="product_name">請輸入要搜索的商品名稱：</label> 輸入得到
        #.get('product_name') 方法用于从 request.POST 字典中获取键为 product_name 的值。


        context = {
            'product_name_pchome': product_name_pchome,
            'pchome_max_pages': pchome_max_pages,
        }

        #调用 scrape_pchome_product 的函数，并将 product_name 作为参数传递给该函数。
        return render(request, 'search_results_pchome.html', context)


def search_form_momo(request):
    return render(request, 'search_form_momo.html')


def search_momo_product_view(request):
    print(request.POST)
    if request.method == 'POST':
        product_name_momo = request.POST.get('product_name_momo')
        print(product_name_momo)
        momo_max_pages = int(request.POST.get('momo_max_pages', 5))
        print(momo_max_pages)

        # 将数据传递给结果模板
        context = {
            'product_name_momo': product_name_momo,
            'momo_max_pages': momo_max_pages
        }
    return render(request, 'search_results_momo.html', context)
    

def search_form_yahoo(request):
    return render(request, 'search_form_yahoo.html')


def search_yahoo_product_view(request):
    #request : HTTP 请求的所有信息，在目前情況下進到http://127.0.0.1:8000/search-form-pchome/這個網頁，輸入要搜尋的名稱，這樣就算是一種request (?
    if request.method == 'POST':
        print(request.POST)
        #用来检查当前 HTTP 请求的方法是否为 POST，參考下方HTTP 请求方法
        product_name_yahoo = request.POST.get('product_name_yahoo')
        print(product_name_yahoo)
        yahoo_max_pages = int(request.POST.get('yahoo_max_pages', 5))
        print(yahoo_max_pages)
        #product_name 是從 <label for="product_name">請輸入要搜索的商品名稱：</label> 輸入得到
        #.get('product_name') 方法用于从 request.POST 字典中获取键为 product_name 的值。
        
        context = {
            'product_name_yahoo': product_name_yahoo,
            'yahoo_max_pages': yahoo_max_pages
        }
        
        #调用 scrape_pchome_product 的函数，并将 product_name 作为参数传递给该函数。
        return render(request, 'search_results_yahoo.html', context) #{'results': context})不能這樣寫，這樣傳給前端會是字典，直接寫context就好
        #簡單來說results的結果會套用到search_results_pchome.html裡面



def pagination_search(request):
    return render(request, 'pagination_search.html')

def pagination_result(request):
    if request.method == 'POST':
        print(request.POST)
        product_name_pchome = request.POST.get('product_name_pchome')
        pchome_max_pages = int(request.POST.get('pchome_max_pages', 5))
        print(product_name_pchome)
        print(pchome_max_pages)

        product_name_momo = request.POST.get('product_name_momo')
        momo_max_pages = int(request.POST.get('momo_max_pages', 5))
        print(product_name_momo)
        print(momo_max_pages)

        product_name_yahoo = request.POST.get('product_name_yahoo')
        yahoo_max_pages = int(request.POST.get('yahoo_max_pages', 5))
        print(product_name_yahoo)
        print(yahoo_max_pages)

        context = {
                'product_name_pchome': product_name_pchome,
                'pchome_max_pages': pchome_max_pages,

                'product_name_momo': product_name_momo,
                'momo_max_pages': momo_max_pages,

                'product_name_yahoo': product_name_yahoo,
                'yahoo_max_pages': yahoo_max_pages,
                }

        return render(request, 'pagination_result.html', context)


def test_but(request):
    return render(request, 'test_but.html')

def test_res(request):

    return render(request, 'test_res.html')

def test_2(request):

    return render(request, 'test_2.html')



#圖片篩選
def image_gallery(request):
    image_dir = settings.MEDIA_ROOT  # 使用 MEDIA_ROOT 指向指定路径

    # 列出目录中的所有支持的图片文件
    supported_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    images = [
        f  # 只需要文件名
        for f in os.listdir(image_dir)
        if os.path.isfile(os.path.join(image_dir, f)) and os.path.splitext(f)[1].lower() in supported_extensions
    ]

    print("检测到的图片：", images)  # 添加此行

    # 使用 Paginator 进行分页，每页显示 20 张图片
    paginator = Paginator(images, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'MEDIA_URL': settings.MEDIA_URL,
    }

    return render(request, 'image_list.html', context)



'''

#處理異步
#這個視圖將會啟動爬蟲並更新狀態。
from django.http import JsonResponse
from django.shortcuts import render
from .tasks import run_scraping_task  # 從 tasks 模塊導入任務

def start_scraping(request):
    # 啟動爬蟲任務
    run_scraping_task.delay()
    return JsonResponse({'status': 'started'})

def check_status(request):
    status = cache.get('scraper_status', 'not_started')
    result = cache.get('scraper_result', [])
    return JsonResponse({'status': status, 'result': result})

def results_page(request):
    return render(request, 'scraper/b_page.html')
'''

















'''
python manage.py runserver
daphne -p 9000 Project_1.asgi:application

遷移數據
python manage.py makemigrations
python manage.py migrate


HTTP 请求方法:
GET：用于请求数据，例如访问一个网页。数据通常通过 URL 查询参数传递。
POST：用于提交数据，例如提交一个表单。数据通常在请求体中传递。
PUT：用于更新数据。
DELETE：用于删除数据。


request.POST：
request.POST 是一个 QueryDict 对象，它类似于 Python 的字典，包含了所有通过 POST 请求提交的表单数据。
每个表单字段的名称作为键，字段的值作为相应的值存储在这个字典状对象中。













'''
