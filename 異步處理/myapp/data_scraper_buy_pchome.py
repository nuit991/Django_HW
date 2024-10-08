from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import asyncio

# 初始化浏览器
def initialize_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

# 进到Pchome，输入商品名称按下enter
def search_product(driver, product_name):
    driver.get("https://24h.pchome.com.tw/")
    driver.implicitly_wait(10)
    search_box = driver.find_element(By.XPATH, '//*[@id="root"]/div/header/div/div[1]/div/div/div/div[1]/div[2]/input')
    search_box.send_keys(product_name)
    search_box.send_keys(Keys.ENTER)
    time.sleep(10)  # 等待页面加载

# 滚动页面加载更多产品
# 根據scroll_count來決定滾動次數，滾到最底一次就是40個項目
def scroll_and_load_more(driver, scroll_count):
    item_container = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ItemContainer")))
    scroll_pause_time = 2  # 每次滚动的停顿时间
    scroll_count_current = 0
    last_count = 0

    #計算滾頁面的次數
    while scroll_count_current < scroll_count:
        # 直接滾到當前頁面的最底
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)

        # 重新获取item_container
        item_container = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ItemContainer")))

        #計算所有商品的個數
        current_count = len(item_container.find_elements(By.CLASS_NAME, "prod_name"))
        # 如果当前数量与上一次相同，说明页面没有加载更多新商品，则退出循环。
        # 代表沒有更多商品了
        if current_count == last_count:
            break
        #每次更新商品數量
        last_count = current_count
        scroll_count_current += 1

    return item_container

# 抓出商品名称 / Url / 价格 / 图片
async def extract_items(driver, item_container):
    item_list = []
    list_items_name = item_container.find_elements(By.CLASS_NAME, "prod_name")
    list_items_price = item_container.find_elements(By.CLASS_NAME, "price")
    list_items_picture = item_container.find_elements(By.CLASS_NAME, "prod_img")

    for name_element, price_element, picture_element in zip(list_items_name, list_items_price, list_items_picture):
        prd_name = name_element.text.strip()
        link_element = name_element.find_element(By.TAG_NAME, "a") if name_element.find_elements(By.TAG_NAME, "a") else None
        product_url = link_element.get_attribute("href") if link_element else "无链接"

        price = price_element.text.strip()
        img_url = picture_element.find_element(By.TAG_NAME, "img").get_attribute("src")

        yield prd_name, product_url, price, img_url
        await asyncio.sleep(1)  # 模拟数据生成的延迟


# 主程序
async def search_pchome_product(product_name, scroll_count):
    retries = 5  # 设置最大重试次数
    attempt = 0

    while attempt < retries:
        try:
            driver = initialize_driver()
            search_product(driver, product_name)
            item_container = scroll_and_load_more(driver, scroll_count)
            #爬商品 / 價錢 / 圖片 / URL
            item_list = extract_items(driver, item_container)

            async for prd_name, product_url, price, img_url in extract_items(driver, item_container):
                yield prd_name, product_url, price, img_url
                await asyncio.sleep(1)  

            break


        except Exception as e:
            print(f"Exception occurred: {str(e)}")
            attempt += 1
            print(f"Retry attempt {attempt}...")

        finally:
            driver.quit()
            time.sleep(2)  # 等待2秒再重试

    print("Reached maximum retries. Returning empty list.")



'''
product_name = '冷氣'
scroll_count = 1
results, total_items = search_pchome_product(product_name, scroll_count)

print(f"找到 {total_items} 个商品:")
print("-" * 20)

for item in results:
    print(f"商品名称: {item[0]}")
    print(f"链接: {item[1]}")
    print(f"价格: {item[2]}")
    print(f"图片: {item[3]}")
    print("-" * 20)
'''