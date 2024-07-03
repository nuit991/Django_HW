# myapp/data_scraper.py

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def init_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://booking-tpsc.sporetrofit.com/Home/LocationPeopleNum")
    driver.implicitly_wait(10)
    return driver

def get_gym_names(driver):
    return [gym_name.text for gym_name in driver.find_elements(By.XPATH, "//h3[@class='tra-heading']")]

def get_people_numbers(driver, cur_xpath, max_xpath):
    current_people = driver.find_element(By.XPATH, cur_xpath).text
    max_people = driver.find_element(By.XPATH, max_xpath).text
    return f"{current_people}/{max_people}"

def scrape_data():
    driver = init_driver()
    gym_names = get_gym_names(driver)
    gyms_info = {
        '北投': (('//*[@id="CurSwPNum_BTSC"]', '//*[@id="MaxSwPNum_BTSC"]'),
                 ('//*[@id="CurGymPNum_BTSC"]', '//*[@id="MaxGymPNum_BTSC"]')),
        '大同': (('//*[@id="CurSwPNum_DTSC"]', '//*[@id="MaxSwPNum_DTSC"]'),
                 ('//*[@id="CurGymPNum_DTSC"]', '//*[@id="MaxGymPNum_DTSC"]')),
        '中正': (('//*[@id="CurSwPNum_JJSC"]', '//*[@id="MaxSwPNum_JJSC"]'),
                 ('//*[@id="CurGymPNum_JJSC"]', '//*[@id="MaxGymPNum_JJSC"]')),
        '南港': (('//*[@id="CurSwPNum_NGSC"]', '//*[@id="MaxSwPNum_NGSC"]'),
                 ('//*[@id="CurGymPNum_NGSC"]', '//*[@id="MaxGymPNum_NGSC"]')),
        '內湖': (('//*[@id="CurSwPNum_NHSC"]', '//*[@id="MaxSwPNum_NHSC"]'),
                 ('//*[@id="CurGymPNum_NHSC"]', '//*[@id="MaxGymPNum_NHSC"]')),
        '士林': (('//*[@id="CurSwPNum_SLSC"]', '//*[@id="MaxSwPNum_SLSC"]'),
                 ('//*[@id="CurGymPNum_SLSC"]', '//*[@id="MaxGymPNum_SLSC"]')),
        '松山': (('//*[@id="CurSwPNum_SSSC"]', '//*[@id="MaxSwPNum_SSSC"]'),
                 ('//*[@id="CurGymPNum_SSSC"]', '//*[@id="MaxGymPNum_SSSC"]')),
        '萬華': (('//*[@id="CurSwPNum_WHSC"]', '//*[@id="MaxSwPNum_WHSC"]'),
                 ('//*[@id="CurGymPNum_WHSC"]', '//*[@id="MaxGymPNum_WHSC"]')),
        '中山': (('//*[@id="CurSwPNum_ZSSC"]', '//*[@id="MaxSwPNum_ZSSC"]'),
                 ('//*[@id="CurGymPNum_ZSSC"]', '//*[@id="MaxGymPNum_ZSSC"]')),
    }

    gym_data = []
    for gym_name in gym_names:
        for gym_name_keyword, (pool_xpaths, gym_xpaths) in gyms_info.items(): #進gyms_info字典做for 迴圈，字典做for迴圈要用.items()
            if gym_name_keyword in gym_name:
                pool_people = get_people_numbers(driver, *pool_xpaths)
                gym_people = get_people_numbers(driver, *gym_xpaths)
                gym_data.append({
                    'name': gym_name,
                    'pool_people': pool_people,
                    'gym_people': gym_people
                })
    driver.quit()
    return gym_data
