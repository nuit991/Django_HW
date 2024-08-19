import asyncio
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

async def scrape_images():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    
    driver = webdriver.Chrome(options=chrome_options)
    url = 'https://e-hentai.org/s/592b6d44de/2771235-1'
    driver.get(url)
    
    sta = 0
    fin = 10

    while sta <= fin:
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        img_tag = soup.find('img', id='img')
        if img_tag:
            img_url = img_tag['src']
            print(img_url)
            yield img_url  # 逐个返回图片 URL
        else:
            break  # 如果没有图片，停止

        try:
            next_page_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'next'))
            )
            next_page_button.click()
            WebDriverWait(driver, 10).until(
                EC.staleness_of(next_page_button)
            )
        except Exception as e:
            break
        sta += 1
        await asyncio.sleep(1)  # 等待一秒钟

    driver.quit()


'''

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import os


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

def scrape_images(sta = 0, page_count = 10):
    # 设置 Chrome 驱动程序选项
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=chrome_options)
    url = 'https://e-hentai.org/s/592b6d44de/2771235-1'
    driver.get(url)
    img_list = []

    while sta <= page_count:
        print(sta)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        img_tag = soup.find('img', id='img')
        if img_tag:
            img_url = img_tag['src']
            img_list.append(img_url)
        else:
            print("No image found")
            break

        try:
            # 查找"下一页"链接并点击
            next_page_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'next'))
            )
            next_page_button.click()

            # 等待新页面加载
            WebDriverWait(driver, 10).until(
                EC.staleness_of(next_page_button)
            )
        except Exception as e:
            print(f"Error navigating to next page: {e}")
            break

        sta += 1
        time.sleep(1) #沒sleep會跳錯(太快來不及抓就按下一頁)

    # 关闭浏览器
    driver.quit()
    return img_list
'''



'''


img_list = scrape_images()

for img in img_list:
    print(img)


'''







