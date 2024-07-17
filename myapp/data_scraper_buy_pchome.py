from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def search_pchome_product(product_name, scroll_count):
    retries = 5  # 设置最大重试次数
    attempt = 0
    item_list = []

    while attempt < retries:
        try:
            # 打开 Chrome 浏览器
            chrome_options = Options()
            chrome_options.add_argument("--headless")  # 无界面模式
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--log-level=3")
            driver = webdriver.Chrome(options=chrome_options)
            driver.get("https://24h.pchome.com.tw/") 
            driver.implicitly_wait(10)

            # 使用 XPath 定位到搜索栏并输入商品名称
            search_box = driver.find_element(By.XPATH, '//*[@id="root"]/div/header/div/div[1]/div/div/div/div/div[2]/input')
            search_box.send_keys(product_name)
            search_box.send_keys(Keys.ENTER)

            # 等待商品列表加载完成
            item_container = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ItemContainer")))



            # 开始滚动页面以加载更多内容
            scroll_pause_time = 2  # 每次滚动的停顿时间
            scroll_count_current = 0
            last_count = 0
            while scroll_count_current < scroll_count:
                # 执行JavaScript来滚动页面到底部
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # 等待一段时间让新内容加载
                time.sleep(scroll_pause_time)

                # 记录当前页面中商品的数量
                current_count = len(item_container.find_elements(By.CLASS_NAME, "prod_name"))

                # 如果商品数量不再增加，则退出循环
                if current_count == last_count:
                    break

                # 更新上一次的商品数量
                last_count = current_count

                # 增加当前滚动次数计数
                scroll_count_current += 1



            # 找到包含商品信息的元素列表
            list_items_name = item_container.find_elements(By.CLASS_NAME, "prod_name")
            list_items_price = item_container.find_elements(By.CLASS_NAME, "price")
            list_items_picture = item_container.find_elements(By.CLASS_NAME, "prod_img")

            # 使用 zip 函数同时迭代名称、价格和图片
            for name_element, price_element, picture_element in zip(list_items_name, list_items_price, list_items_picture):
                # 获取商品名称和链接
                item_text = name_element.text.strip()
                link_element = name_element.find_element(By.TAG_NAME, "a")
                item_url = link_element.get_attribute("href")

                # 获取价格
                price_text = price_element.text.strip()

                # 获取图片链接
                picture_src = picture_element.find_element(By.TAG_NAME, "img").get_attribute("src")

                # 加入到商品列表中
                item_list.append((item_text, item_url, price_text, picture_src))

            #print(f"Total items found: {len(item_list)}")
            total_items = len(item_list)
            return item_list, total_items

        except Exception as e:
            print(f"Exception occurred: {str(e)}")
            attempt += 1
            print(f"Retry attempt {attempt}...")

        finally:
            driver.quit()
            time.sleep(2)  # 等待2秒再重试

    print("Reached maximum retries. Returning empty list.")
    return []

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