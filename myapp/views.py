from django.shortcuts import render #將一個模板和數據組合在一起，生成一個渲染後的 HTML 響應，然後將該響應返回給用戶端。
from django.http import JsonResponse  #Django 框架中导入 JsonResponse 类的语句。它用于在 Django 视图中创建和返回 JSON 响应
from .data_scraper import scrape_data

def home(request):  #当用户第一次访问网站时，Django 会调用这个视图。
    gym_data = scrape_data()
    return render(request, 'home.html', {'gym_data': gym_data})

def gym_data_api(request):  #用于提供动态数据更新的 API 端点。
    gym_data = scrape_data()
    return JsonResponse({'gym_data': gym_data})
