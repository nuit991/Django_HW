from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

def search_momo_product(product_name, max_pages):
    retries = 3  # 最大重试次数
    attempt = 0
    item_list = []
    total_items = 0

    while attempt < retries:
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--log-level=3")
            driver = webdriver.Chrome(options=chrome_options)
            driver.get("https://www.momoshop.com.tw/main/Main.jsp")
            driver.implicitly_wait(10)

            # 使用 XPath 定位搜索框并输入商品名称
            search_box = driver.find_element(By.XPATH, '//*[@id="keyword"]')
            search_box.send_keys(product_name)
            search_box.send_keys(Keys.ENTER)
            time.sleep(10)
            
            html_source = driver.page_source
            soup = BeautifulSoup(html_source, 'html.parser')

            item_containers = soup.find_all('li', attrs={'gcode': True})
            print(len(item_containers))
            current_page = 1
            page_number = current_page
            page_number
            while current_page <= max_pages: 
                print(f"Scraping page {current_page}...")

                
                for item_container in item_containers:
                    prd_name = item_container.find('h3', class_='prdName').text.strip()
                    #print(prd_name)
                    price = item_container.find('span', class_='price').text.strip()
                    #print(price)
                    product_url_good = item_container.find('a', class_='goodsUrl')['href']
                    product_url = 'https://www.momoshop.com.tw' + product_url_good
                    #print(product_url)
                    img_tag = item_container.find('img', class_='prdImg')
                    img_url = img_tag['src']
                    #print(img_url)
                    

                    item_list.append((prd_name, product_url, price, img_url))

                # 找到下一页按钮并点击
                try:
                    if current_page <= 11:
                        css_selector = f'#BodyBase > div.bt_2_layout.searchbox.searchListArea.selectedtop > div:nth-child(6) > ul > li:nth-child({page_number}) > a'
                        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector)))
                        element.click()
                        print(f'第{current_page} OK')
                        time.sleep(5)
                        current_page += 1
                        page_number = current_page
                    else:
                        page_number = (current_page % 10) + 2
                        css_selector = f'#BodyBase > div.bt_2_layout.searchbox.searchListArea.selectedtop > div:nth-child(6) > ul > li:nth-child({page_number}) > a'
                        # 使用 CSS 選擇器定位元素並點擊
                        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector)))
                        element.click()
                        print(f'第{current_page} OK')
                        time.sleep(5)
                        WebDriverWait(driver, 20).until(EC.staleness_of(element))
            
                        current_page += 1

                except Exception as e:
                    print(f"No more pages or error occurred: {str(e)}")
                    break

            #print(f"Total 'Next Page' clicks: {current_page - 1}")  # 打印点击下一页次数
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
    return item_list, total_items

'''

# 要搜索的商品名称
product_name = '冷氣'
results, total_items = search_momo_product(product_name, max_pages=5)

# 输出搜索结果
for item in results:
    print(f"商品名称: {item[0]}")
    print(f"链接: {item[1]}")
    print(f"价格: {item[2]}")
    print(f"图片: {item[3]}")
    print("-" * 20)
''' 
