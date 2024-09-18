from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import os
from urllib.parse import urlparse, unquote
import requests
from urllib.parse import urljoin


chrome_options = Options()
#chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--log-level=3")  
driver = webdriver.Chrome(options=chrome_options)

driver.get("https://sv-uploader.illgames.jp/characters")
driver.implicitly_wait(10)
driver.maximize_window()



#下載路徑
download_dir = 'E:/img_123'
os.makedirs(download_dir, exist_ok=True)
base_url = 'https://sv-uploader.illgames.jp/characters?sex=1&page=85'

num = 86

while num <= 1000:
    #soup處理
    html_source = driver.page_source
    soup = BeautifulSoup(html_source, 'html.parser')
    all_pic = soup.find('div', class_='p-1 lg:p-6')
    all_pic_1 = all_pic.find('div', class_='grid gap-1 md:grid-cols-2 xl:grid-cols-[repeat(auto-fill,minmax(26rem,1fr))] lg:gap-6')
    all_pic_2 = all_pic_1.find_all('div', class_='@container relative flex aspect-[8/5] w-full gap-1 overflow-hidden rounded-xl border border-border bg-[length:24px_24px] bg-sky-400 bg-stripes p-2 shadow-sm dark:bg-sky-900')

    for x_1 in all_pic_2:
    
        te_1 = x_1.find('div', class_='group relative h-full w-[calc(44.74%-0.25rem)] shrink-0 rounded-md bg-gray-300')
        #print(te_1)
        te_2 = te_1.find('div', class_='pointer-events-none absolute bottom-0 w-full p-2 opacity-0 transition-all group-hover:pointer-events-auto motion-safe:group-hover:scale-100 motion-safe:scale-95 focus-within:opacity-100 group-hover:opacity-100')
        #print(te_2)
        te_3 = te_2.find('a')['href']
        #print(te_3)
        full_url = urljoin(base_url, te_3)

        file_name = os.path.basename(te_3)
        file_path = os.path.join(download_dir, file_name)

        response = requests.get(full_url)
        if response.status_code == 200:
            with open(file_path, 'wb') as file:
                file.write(response.content)
                print(f"Downloaded: {file_name}")
        else:
            print(f"Failed to download {file_name}, status code: {response.status_code}")
    aria_label = f"ページ {num}"
    next_page_button = driver.find_element(By.XPATH, f'//a[@aria-label="{aria_label}"]')
    next_page_button.click()
    print(num)
    num += 1
    time.sleep(1)