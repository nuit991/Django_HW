from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

def search_momo_product(product_name):
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
            driver.get("https://www.momoshop.com.tw/main/Main.jsp") # 更改網址以前往不同網頁
            driver.implicitly_wait(10)

            # 使用 XPath 定位到搜索欄位並輸入商品名稱
            search_box = driver.find_element(By.XPATH, '//*[@id="keyword"]')
            search_box.send_keys(product_name)
            search_box.send_keys(Keys.ENTER)

            # 等待商品列表加載完畢
            item_containers = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "listAreaLi")))


            # 使用 zip 函數來同時迭代名稱和價格
            for item_container in item_containers[:10]:
                prd_name = item_container.find_element(By.CLASS_NAME, "prdName").text
                # 獲取價格
                price = item_container.find_element(By.CLASS_NAME, "price").text
                # 獲取商品連結
                link_element = item_container.find_element(By.CSS_SELECTOR, "a.goods-img-url")
                product_url = link_element.get_attribute("href")             

                # 將資料加入到 item_list 中
                item_list.append((prd_name, product_url, price))

            return item_list

        except Exception as e:
            print(f"Exception occurred: {str(e)}")
            attempt += 1
            print(f"Retry attempt {attempt}...")

        finally:
            driver.quit()
            time.sleep(2)  # 等待2秒再重試

    print("Reached maximum retries. Returning empty list.")
    return []

'''

# 要搜索的商品名稱
product_name = '冷氣'
results = search_momo_product(product_name)

# 輸出搜索結果
for item in results:
    print(f"商品名稱: {item[0]}")
    print(f"連結: {item[1]}")
    print(f"價格: {item[2]}")
    print("-" * 20)
    
'''