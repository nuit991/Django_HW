from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

#初始化瀏覽器
def initialize_driver():
    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

#進到momo商城，輸入商品名稱按下enter
def search_product(driver, product_name):
    driver.get("https://www.momoshop.com.tw/main/Main.jsp")
    driver.implicitly_wait(10)
    search_box = driver.find_element(By.XPATH, '//*[@id="keyword"]')
    search_box.send_keys(product_name)
    search_box.send_keys(Keys.ENTER)
    time.sleep(10)  # 等待页面加载

#用BeautifulSoup抓下整個網頁
def get_page_content(driver):
    html_source = driver.page_source
    soup = BeautifulSoup(html_source, 'html.parser')
    #print('soup', soup)
    return soup

#找到商品標籤，抓取名稱 / Url / 價錢 / 圖片
def parse_product_info(soup):
    item_list = []
    list_area_div_1 = soup.find('div', class_='listArea')
    list_area_div = list_area_div_1.find_all('li')
    print(len(list_area_div))
    #item_containers = list_area_div.find('ul', class_='clearfix')
    #print('item_containers', item_containers)
    #print(len(item_containers))
    for item_container in list_area_div:
        prd_name = item_container.find('h3', class_='prdName').text.strip()
        print('prd_name', prd_name)

        #money_div = item_container.find('div', class_='money')
        #price_1 = money_div.find('span', class_='price')
        #price_2 = price_1.find('i', class_='icon icon-dollar-sign')
        price = item_container.find('span', class_='price').find('b').text.strip()
        print('price', price)

        #product_url_good = item_container.find('div', class_='swiper-slide swiper-slide-active')
        product_url_good = item_container.find('a', class_='goodsUrl')['href']
        #print('product_url_good', product_url_good)
        product_url = 'https://www.momoshop.com.tw' + product_url_good 
        #product_url = product_url_1
        print('product_url', product_url)

        img_tag = item_container.find('img', class_='prdImg')
        img_url = img_tag['src']
        print('img_url', img_url)
        item_list.append((prd_name, product_url, price, img_url))
    return item_list

#點下一頁
def click_next_page(driver, current_page):
    # 找到下一页按钮并点击
    page_number = current_page
    try:
        #momo下一頁標籤的編號最多到11
        #要先點下十頁(標籤數字是11)，才能到下10頁，不會點第10頁就自動顯示11、12、13頁...
        if current_page <= 11:
            css_selector = f'#BodyBase > div.bt_2_layout.searchbox.searchListArea.selectedtop > div:nth-child(6) > ul > li:nth-child({page_number}) > a'
            element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector)))
            element.click()
            print(f'第{current_page} OK')
            time.sleep(5)
            
            #這邊用page_number = current_page是為了第12頁網頁的標籤數字會變回4，之後丟給else處理
            page_number = current_page
        else:
            #第12頁開始的規律都是(current_page % 10) + 2，current_page是我自己數的，網頁的標籤數字是4
            page_number = (current_page % 10) + 2
            css_selector = f'#BodyBase > div.bt_2_layout.searchbox.searchListArea.selectedtop > div:nth-child(6) > ul > li:nth-child({page_number}) > a'
            # 使用 CSS 選擇器定位元素並點擊
            element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector)))
            element.click()
            print(f'第{current_page} OK')
            time.sleep(5)
            WebDriverWait(driver, 20).until(EC.staleness_of(element))
            

    except Exception as e:
        print(f"No more pages or error occurred: {str(e)}")


#主要執行程式
def search_momo_product(product_name, max_pages):
    retries = 5
    attempt = 0
    item_list = []
    total_items = 0

    #若失敗的重複迴圈
    while attempt < retries:
        try:
            driver = initialize_driver()
            search_product(driver, product_name)
            current_page = 1
            #User決定最大搜尋頁數
            while current_page <= max_pages:
                print(f"Scraping page {current_page}...")
                soup = get_page_content(driver)
                item_list.extend(parse_product_info(soup))  
                click_next_page(driver, current_page)
                current_page += 1

            total_items = len(item_list)
            print(f"Page {current_page}: {total_items} products found.")
            return item_list, total_items

        except Exception as e:
            print(f"Exception occurred: {str(e)}")
            attempt += 1
            print(f"Retry attempt {attempt}...")

        finally:
            driver.quit()
            time.sleep(2)

    print("Reached maximum retries. Returning empty list.")
    return item_list, total_items


'''
# 要搜索的商品名称
product_name = '冷氣'
results, total_items = search_momo_product(product_name, max_pages=1)

# 输出搜索结果
for item in results:
    print(f"商品名称: {item[0]}")
    print(f"链接: {item[1]}")
    print(f"价格: {item[2]}")
    print(f"图片: {item[3]}")
    print("-" * 20)
'''
