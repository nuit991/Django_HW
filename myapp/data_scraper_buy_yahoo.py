import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time


def search_yahoo_product(product_name):
    retries = 100  # 設定最大重試次數
    attempt = 0
    item_list = []
    
    while attempt < retries:
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--log-level=3")
            driver = webdriver.Chrome(options=chrome_options)
            
            driver.get("https://tw.buy.yahoo.com/") # 更改網址以前往不同網頁
            driver.implicitly_wait(10)

            # 使用 XPath 定位到搜索欄位並輸入商品名稱
            search_box = driver.find_element(By.XPATH, '//*[@id="UH_SAS"]/div[2]/div[2]/div/div/form/input[1]')
            search_box.send_keys(product_name)
            search_box.send_keys(Keys.ENTER)

            # 使用 WebDriverWait 等待搜索結果加載
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.sc-1drl28c-1.cnHJYW')))
            
            # 獲取 HTML 內容
            html_content = driver.page_source
        
            # 使用 BeautifulSoup 解析 HTML
            soup = BeautifulSoup(html_content, 'html.parser')

            # 找出所有符合條件的商品元素
            product_elements = soup.find_all('a', class_='sc-1drl28c-1 cnHJYW')
            
            # 遍歷並處理每個商品元素
            for product in product_elements:
                try:
                    # 提取商品名稱
                    prd_name = product.find('span', class_='sc-dlyefy sc-gKcDdr sc-1drl28c-5 jHwfYO ikfoIQ jZWZIY').text.strip()
                    # 提取商品 price
                    price = product.find('span', class_='sc-dlyefy sc-gKcDdr dfRcqf hFXgfs').text.strip()
                    # 提取商品 url
                    url = product['href']
                    # 提取商品 圖片
                    #使用一個一個點進商品來抓的方式
                    if url:
                        try:
                            driver.get(url) 
                            html = driver.page_source
                            soup = BeautifulSoup(html, 'html.parser')
                            #print(soup)
                            img_wrapper = soup.find('div', class_='LensImage__imgWrapper___SXnau')
                            #print(img_wrapper)
                            img_urls = []
                            if img_wrapper:
                                img_tags = img_wrapper.find_all('img')
                                for img in img_tags:
                                    img_url = img.get('src')
                                    if img_url and img_url.endswith('.jpg'):
                                        img_urls.append(img_url)

                            if not img_urls:   # 這樣寫的話 img_urls 表示為empty or False，如果是寫 if img_urls == None則是只有表示為None
                                img_wrapper = soup.find_all('span', class_='ImageHover__thumbnail___1YTO5')
                                if img_wrapper:
                                    img_tags = img_wrapper[1]
                                    img_tags_1 = img_tags.find_all('img')
                                    for img in img_tags_1:
                                        img_url = img.get('src')
                                        if img_url and img_url.endswith('.jpg'):
                                            img_urls.append(img_url)
                                            
                            #print(img_tags)
                            #print(img_urls)
                            #print('\n')
                        except AttributeError as e:
                            print(f"Error extracting product details: {str(e)}")
                        #product_span = product_img.find('span', class_='ImageHover__thumbnail___1YTO5')
                        #print(product_span)
                        # 提取商品價格
    
                    item_list.append((prd_name, url, price, img_urls))
                except AttributeError as e:
                    print(f"Error extracting product details: {str(e)}")

            driver.quit()


            #這邊處理[123,[ABC]]的問題
            flattened_data = []
            # 遍历原始数据
            for item in item_list:
                prd_name, url, price, img_urls = item
                if isinstance(img_urls, list) and img_urls:
                    # 提取列表中的第一个图片 URL
                    img_url = img_urls[0]
                else:
                    img_url = img_urls  # 如果已经是字符串，直接使用
    
                # 将扁平化后的数据项添加到新的列表中
                flattened_data.append((prd_name, url, price, img_url))

            return flattened_data

        except Exception as e:
            print(f"Exception occurred: {str(e)}")
            attempt += 1
            print(f"Retry attempt {attempt}...")
            driver.quit()

    print(f"Failed after {retries} retries. Exiting...")
    return item_list

'''
product_name = '手機殼'
results = search_yahoo_product(product_name)


# 輸出搜索結果
for item in results:
    print(f"商品名稱: {item[0]}")
    print(f"連結: {item[1]}")
    print(f"價格: {item[2]}")
    print(f"圖片: {item[3]}")
    print("-" * 20)
'''
