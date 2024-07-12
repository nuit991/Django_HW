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
            #WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.sc-1drl28c-1.cnHJYW')))
            
            # 獲取 HTML 內容
            html_content = driver.page_source
        
            # 使用 BeautifulSoup 解析 HTML
            soup = BeautifulSoup(html_content, 'html.parser')

            # 找出所有符合條件的商品元素
            product_elements = soup.find_all('a', class_='sc-1drl28c-1 cnHJYW') #先定位這條，Yahoo的這部分是最上層
        
            # 遍歷並處理每個商品元素
            for product in product_elements[:10]:
                # 提取商品名稱
                prd_name = product.find('span', class_='sc-dlyefy sc-gKcDdr sc-1drl28c-5 jHwfYO ikfoIQ jZWZIY').text.strip()
                
                # 提取商品 URL
                url = product['href']

                # 提取商品價格
                price = product.find('span', class_='sc-dlyefy sc-gKcDdr dfRcqf hFXgfs').text.strip()
                
                item_list.append((prd_name, url, price))
            
            driver.quit()
            return item_list

        except AttributeError as e:
            print(f"Exception occurred: {str(e)}")
            attempt += 1
            print(f"Retry attempt {attempt}...")
            driver.quit()

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