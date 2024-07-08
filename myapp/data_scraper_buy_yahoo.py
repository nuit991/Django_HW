import requests
from bs4 import BeautifulSoup


def search_yahoo_product(product_name):
    retries = 100  # 設定最大重試次數
    attempt = 0
    item_list = []
    while attempt < retries:
        try:
            url = "https://tw.buy.yahoo.com/search/product?p=iphone%2015"

            # 發送 GET 請求並取得 HTML 內容
            response = requests.get(url)
            html_content = response.text

            # 使用 BeautifulSoup 解析 HTML
            soup = BeautifulSoup(html_content, 'html.parser')

            # 找出所有符合條件的商品元素
            product_elements = soup.find_all('a', class_='sc-1drl28c-1 cnHJYW')
        
            # 遍歷並處理每個商品元素
            for product in product_elements:
            
                # 提取商品名稱
                prd_name = product.find('span', class_='sc-dlyefy sc-gKcDdr sc-1drl28c-5 jHwfYO ikfoIQ jZWZIY').text.strip()

                # 提取商品 URL
                url = product['href']

                # 提取商品價格
                price = product.find('span', class_='sc-dlyefy sc-gKcDdr dfRcqf hFXgfs').text.strip()
                item_list.append((prd_name, url, price))
            return item_list

        except AttributeError as e:
            print(f"Exception occurred: {str(e)}")
            attempt += 1
            print(f"Retry attempt {attempt}...")


'''

product_name = '冷氣'
results = search_yahoo_product(product_name)

# 輸出搜索結果
for item in results:
    print(f"商品名稱: {item[0]}")
    print(f"連結: {item[1]}")
    print(f"價格: {item[2]}")
    print("-" * 20)
    
'''