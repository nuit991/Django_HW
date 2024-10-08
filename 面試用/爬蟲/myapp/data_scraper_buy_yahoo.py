import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import asyncio

#初始化瀏覽器
def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # For headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

#輸入商品名稱後Enter
def search_product_on_yahoo(driver, product_name):
    driver.get("https://tw.buy.yahoo.com/")
    driver.implicitly_wait(10)
    search_box = driver.find_element(By.XPATH, '//*[@id="UH_SAS"]/div[2]/div[2]/div/div/form/input[1]')
    search_box.send_keys(product_name)
    search_box.send_keys(Keys.ENTER)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.sc-1drl28c-1.cnHJYW')))

    # 第1次更新全商品網址
    current_url = driver.current_url

    return current_url

#頁面滾到底，不然有些商品不會顯示
def scroll_to_bottom(driver):
    scroll_step = 1000
    while True:
        driver.execute_script(f"window.scrollBy(0, {scroll_step});")
        time.sleep(0.5)
        if driver.execute_script("return window.innerHeight + window.scrollY") >= driver.execute_script("return document.body.scrollHeight"):
            break

#顯示商品數量，然後提取名稱 / Url / 金額 / 圖片
async def extract_product_info(driver, current_page):
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    product_elements = soup.find_all('a', class_='sc-1drl28c-1 cnHJYW')
    
    # 打印當成商品數量
    if current_page == 6:
        print(f"Page {current_page}: {len(product_elements)} products found.")
    else:
        print(f"Page {current_page}: {len(product_elements)} products found.")
    

    for product in product_elements:
        try:
            # 提取商品 name 不要先+.text.strip()，不然他抓不到就會直接掛掉
            prd_name_element = product.find('span', class_='sc-dlyefy sc-gKcDdr sc-1drl28c-5 jHwfYO ikfoIQ jZWZIY')
            if prd_name_element:
                prd_name = prd_name_element.text.strip()
            else:
                prd_name_element = product.find('span', class_='sc-gKcDdr sc-jMupca sc-1drl28c-5 kfLbyM hOVTkx jZWZIY')
                if prd_name_element:
                    prd_name = prd_name_element.text.strip()
            print('prd_name: ', prd_name)



            # 提取商品 price
            price_element = product.find('span', class_='sc-dlyefy sc-gKcDdr dfRcqf hFXgfs')
            if price_element:
                price = price_element.text.strip()
            else:
                price_element = product.find('span', class_='sc-gKcDdr sc-jMupca ETTiJ esZnNV')
                if price_element:
                    price = price_element.text.strip()
            print('price: ', price)

    
            # 提取商品 url
            product_url = product['href']
            print('product_url: ', product_url)

            img_urls = extract_product_images(driver, product_url)
            

        except AttributeError as e:
            print(f"Error extracting product details: {str(e)}")


        # 遍历原始数据
        # isinstance : img_urls 是一个列表，它会返回 True；否则，返回 False。
        if isinstance(img_urls, list) and img_urls:
        # 提取列表中的第一个图片 URL
            img_url = img_urls[0]
        else:
            img_url = img_urls  # 如果已经是字符串，直接使用
        print('img_urls: ', img_url)

        yield prd_name, product_url, price, img_url


#圖片要點進去抓，多寫一個def
def extract_product_images(driver, product_url):
    img_urls = []
    try:
        driver.get(product_url)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        #圖片位子
        img_wrapper = soup.find('div', class_='LensImage__imgWrapper___SXnau')
        if img_wrapper:
            img_tags = img_wrapper.find_all('img')
            # .endswith 檢查是否以 ".jpg" / '.jpeg' 结尾
            img_urls = [img.get('src') for img in img_tags if img.get('src') and (img.get('src').endswith('.jpg') or img.get('src').endswith('.jpeg'))]
            time.sleep(1)
        else:
            #圖片位子
            img_wrapper = soup.find_all('span', class_='ImageHover__thumbnail___1YTO5')
            if img_wrapper:
                img_tags = img_wrapper[1].find_all('img')
                img_urls = [img.get('src') for img in img_tags if img.get('src') and (img.get('src').endswith('.jpg') or img.get('src').endswith('.jpeg'))]
                time.sleep(1)
    except Exception as e:
        print(f"Failed to extract images for product URL: {product_url}")
        print(f"Error: {str(e)}")
    return img_urls

#點下一頁
def click_next_page(driver, current_page):
    try:
        #網站點到第4頁，第5頁他的current_page會保持在4
        if current_page == 4:
            css_selector = f'#isoredux-root > div.page.shopping.disableUserSelectInTouchDevice.Layout_layoutBg_3R7Zt > div:nth-child(1) > div.pageFlex > div > div.Pagination_pagination_uC5J7 > div > div > a:nth-child({current_page})'
        #用兩個判斷是確定他會在current_page = 4之前套用
        if current_page != 4 and current_page < 4:
            css_selector = f'#isoredux-root > div.page.shopping.disableUserSelectInTouchDevice.Layout_layoutBg_3R7Zt > div:nth-child(1) > div.pageFlex > div > div.Pagination_pagination_uC5J7 > div > div > a:nth-child({current_page + 1})'
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector)))
        element.click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.sc-1drl28c-1.cnHJYW')))
        #第2次更新權商品網址
        
        return True
    except Exception as e:
        print(f"Failed to click on page {current_page + 1} button: {str(e)}")
        return False

#主要程式
async def search_yahoo_product(product_name, max_pages):
    driver = None
    retries = 5
    attempt = 0
    len_item_list = 0
    print('product_name', product_name)
    print('max_pages', max_pages)
    #若有問題會重試
    while attempt < retries:
        try:
            driver = setup_driver()
            search_product_on_yahoo(driver, product_name)
            current_page = 1
            
            #User決定要抓取的最大頁數
            while current_page <= max_pages:
                #往下滑，不然有些商品不會顯示
                scroll_to_bottom(driver)
                    
                #抓商品資料
                async for prd_name, product_url, price, img_url in extract_product_info(driver, current_page):
                    yield prd_name, product_url, price, img_url
                    await asyncio.sleep(1) 

                if current_page == 1:
                    current_url =  search_product_on_yahoo(driver, product_name) #返回current_url(會再重複一次輸入商品名稱然後按下搜尋的動作)
                    #print(current_url)
                    #回到全品商品的那一頁
                    driver.get(current_url)
                    #按下一頁
                    click_next_page(driver, current_page)
                    time.sleep(5)
                    current_page += 1
                    current_url = driver.current_url
                else:
                    driver.get(current_url)
                    click_next_page(driver, current_page)  
                    time.sleep(5) 
                    #print(current_url)
                    current_url = driver.current_url
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
# 測試搜索功能
product_name = '牙刷'
max_page = 2
results, len_item_list = search_yahoo_product(product_name, max_page)



# 輸出搜索結果
for item in results:
    print(f"商品名稱: {item[0]}")
    print(f"連結: {item[1]}")
    print(f"價格: {item[2]}")
    print(f"圖片: {item[3]}")
    print("-" * 20)




img_urls = [img.get('src') for img in img_tags if img.get('src') and (img.get('src').endswith('.jpg') or img.get('src').endswith('.jpeg'))]
不用列表推倒式
# 初始化空列表来存储图片 URL
img_urls = []

# 遍历 img_tags 中的每一个 img 标签
for img in img_tags:
    # 获取 img 标签的 'src' 属性
    src = img.get('src')
    
    # 检查 'src' 是否存在且非空
    if src:
        # 检查 'src' 是否以 .jpg 或 .jpeg 结尾
        if src.endswith('.jpg') or src.endswith('.jpeg'):
            # 如果符合条件，将 'src' 添加到 img_urls 列表中
            img_urls.append(src)

# 输出结果
print(img_urls)



'''