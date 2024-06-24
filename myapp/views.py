from django.shortcuts import render #將一個模板和數據組合在一起，生成一個渲染後的 HTML 響應，然後將該響應返回給用戶端。
from django.http import JsonResponse  #Django 框架中导入 JsonResponse 类的语句。它用于在 Django 视图中创建和返回 JSON 响应
from .data_scraper import scrape_data

def home(request):  #当用户第一次访问网站时，Django 会调用这个视图。
    gym_data = scrape_data()
    return render(request, 'home.html', {'gym_data': gym_data})

def gym_data_api(request):  #用于提供动态数据更新的 API 端点。
    gym_data = scrape_data()
    return JsonResponse({'gym_data': gym_data})



'''
from .data_scraper import scrape_data
->從data_scraper.py匯入scrape_data這個函式

return render(request, 'home.html', {'gym_data': gym_data})
0.用在網頁打開時顯示的項目(粗略來說)
1.{'gym_data': gym_data}: 是一个字典，它将会传递给模板引擎，用于填充模板中的变量。在这里，'gym_data' 是模板中可以使用的变量名，gym_data 是从 scrape_data() 函数获取的数据。
2.'home.html': 是要渲染的模板文件的名称或路径
3.request: 这是一个包含了客户端请求信息的对象。它传递给视图函数，以便视图函数可以根据请求的内容进行处理，并生成相应的 HTML 页面返回给用户。(?)

return JsonResponse({'gym_data': gym_data})
0.用在動態數值的顯示(粗略來說)

''''
