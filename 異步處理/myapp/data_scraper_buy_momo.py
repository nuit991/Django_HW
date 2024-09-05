#抓不到就一個一個慢慢定位，從父層開始定子層，慢慢定下來
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import asyncio

#初始化瀏覽器
def initialize_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
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
    return soup

#找到商品標籤，抓取名稱 / Url / 價錢 / 圖片
async def parse_product_info(soup):
    list_area_div = soup.find('div', class_='listArea')
    item_containers = list_area_div.find('ul', class_='clearfix')
    #print('item_containers', item_containers)
    print(len(item_containers))
    for item_container in item_containers:
        prd_name = item_container.find('h3', class_='prdName').text.strip()

        money_div = item_container.find('p', class_='money')
        price = money_div.find('span', class_='price').text.strip()

        product_url = 'https://www.momoshop.com.tw' + item_container.find('a', class_='goodsUrl')['href']

        img_tag = item_container.find('img', class_='prdImg')
        img_url = img_tag['src']

        print(img_url)
        yield prd_name, product_url, price, img_url
        await asyncio.sleep(1)  # 模拟数据生成的延迟

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
async def search_momo_product(product_name, max_pages):
    retries = 5
    attempt = 0

    #若失敗的重複迴圈
    while attempt < retries:
        try:
            driver = initialize_driver()
            search_product(driver, product_name)
            current_page = 1
            #User決定最大搜尋頁數
            while current_page <= max_pages:
                print('current_page: ', current_page)
                print(f"Scraping page {current_page}...")
                soup = get_page_content(driver)
                #print('OKOK_1')
                async for prd_name, product_url, price, img_url in parse_product_info(soup):
                    yield prd_name, product_url, price, img_url
                    await asyncio.sleep(1)  
                click_next_page(driver, current_page)
                current_page += 1

            break #沒加break他會一直抓   

        except Exception as e:
            print(f"Exception occurred: {str(e)}")
            attempt += 1
            print(f"Retry attempt {attempt}...")

        finally:
            driver.quit()
            time.sleep(2)

    print("Reached maximum retries. Returning empty list.")
    await asyncio.sleep(1)  # 模拟数据生成的延迟




'''

# 要搜索的商品名称
async def main():
    product_name = '冷氣'
    max_pages = 3

    async for product in search_momo_product(product_name, max_pages):
        print(f'Product Name: {product["prd_name"]}')
        print(f'Product URL: {product["product_url"]}')
        print(f'Price: {product["price"]}')
        print(f'Image URL: {product["img_url"]}')

if __name__ == '__main__':
    asyncio.run(main())

'''

