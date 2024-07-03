from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def search_pchome_product(product_name):
    # 開啟 Chrome 瀏覽器
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://24h.pchome.com.tw/") 
    driver.implicitly_wait(10)

    try:
        # 使用 XPath 定位到搜索欄位並輸入商品名稱
        search_box = driver.find_element(By.XPATH, '//*[@id="root"]/div/header/div/div[1]/div/div/div/div/div[2]/input')
        search_box.send_keys(product_name)
        search_box.send_keys(Keys.ENTER)

        item_list = []

        # 等待商品列表加載完畢
        item_container = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ItemContainer")))

        # 找到含有 prod_name 的元素
        list_items_name = item_container.find_elements(By.CLASS_NAME, "prod_name")
        list_items_price = item_container.find_elements(By.CLASS_NAME, "price")

        # 使用 zip 函數來同時迭代名稱和價格
        for name_element, price_element in zip(list_items_name, list_items_price):
            # 取得商品名稱
            item_text = name_element.text.strip()

            # 在每個 prod_name 元素下找到內部的 <a> 標籤
            link_element = name_element.find_element(By.TAG_NAME, "a")

            # 取得連結 URL
            item_url = link_element.get_attribute("href")

            # 取得價格
            price_text = price_element.text

            # 加入到商品列表中
            item_list.append((item_text, item_url, price_text))

            # 如果已經處理了10個商品，就退出迴圈
            if len(item_list) >= 10:
                break

        return item_list

    finally:
        driver.quit()


'''
# 讓使用者輸入商品名稱
product_name = input("請輸入要搜索的商品名稱：")
results = search_pchome_product(product_name)

# 輸出搜索結果
for item in results:
    print(f"商品名稱: {item[0]}")
    print(f"連結: {item[1]}")
    print(f"價格: {item[2]}")
    print("-" * 20)

'''
