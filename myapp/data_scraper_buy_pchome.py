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
    driver.get("https://24h.pchome.com.tw/")
    driver.implicitly_wait(10)
    search_box = driver.find_element(By.XPATH, '//*[@id="root"]/div/header/div/div[1]/div/div/div/div[1]/div/div[3]/input')
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
    #這邊要一層一層處理，直接用div抓下面商品的標籤，像這邊就是li，跳過ul的標籤沒關係
    list_area_div_1 = soup.find('div', class_='c-listInfoGrid__body')
    #list_area_div_2 = list_area_div_1.find_all('ul', class_='c-listInfoGrid__list c-listInfoGrid__list--wrapProdCard')
    list_area_div = list_area_div_1.find_all('li', class_ = 'c-listInfoGrid__item c-listInfoGrid__item--gridCardGray5')
    #print(len(list_area_div))
    #item_containers = list_area_div.find('ul', class_='clearfix')
    #print('item_containers', item_containers)
    #print(len(item_containers))
    for item_container in list_area_div[1:]:
        #print(item_container)
        prd_name = item_container.find('div', class_='c-prodInfoV2__title').text.strip()
        #print('prd_name', prd_name)

        #money_div = item_container.find('div', class_='money')
        #price_1 = money_div.find('span', class_='price')
        #price_2 = price_1.find('i', class_='icon icon-dollar-sign')
        price = item_container.find('div', class_='c-prodInfoV2__priceValue c-prodInfoV2__priceValue--m').text.strip()
        #print('price', price)

        product_url_good = item_container.find('a', class_='c-prodInfoV2__link gtmClickV2')['href'].strip()
        product_url = 'https://24h.pchome.com.tw' + product_url_good 
        #product_url = product_url_1
        #print('product_url', product_url)

        img_tag = soup.find('div', class_='c-prodInfoV2__img').find('img')
        if img_tag:
            img_url = img_tag['src']
        else:
            print("Image tag not found.")

        #print('img_url', img_url)
        item_list.append((prd_name, product_url, price, img_url))
    return item_list

#點下一頁
def click_next_page(driver, current_page):
    # 找到下一页按钮并点击
    try:

        if current_page == 1 :
            css_selector = f'/html/body/div[1]/main/div[1]/div/div/section[2]/div/div/section/div/div[2]/div/div[3]/div/ul/li[2]/a'
            element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, css_selector)))
            element.click()
            print(f'第{current_page} OK')
            time.sleep(5)

        elif current_page > 1 & current_page <= 5 : 
            css_selector = f'/html/body/div[1]/main/div[1]/div/div/section[2]/div/div/section/div/div[2]/div/div[3]/div/ul/li[{current_page}]/a'
            element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, css_selector)))
            element.click()
            print(f'第{current_page} OK')
            time.sleep(5)

            #PChome下一頁標籤最多到li[6]
        else:
            css_selector = f'/html/body/div[1]/main/div[1]/div/div/section[2]/div/div/section/div/div[2]/div/div[3]/div/ul/li[6]/a'
            element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, css_selector)))
            element.click()
            print(f'第{current_page} OK')
            time.sleep(5)
            
            

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

            if max_pages == 1:
                current_page == max_pages
                print(f"Scraping page {current_page}...")
                soup = get_page_content(driver)
                item_list.extend(parse_product_info(soup))

            else:
                
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
