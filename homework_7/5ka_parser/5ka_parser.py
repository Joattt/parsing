from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pymongo import MongoClient

service = Service('chromedriver.exe')
driver = webdriver.Chrome(service=service)
driver.maximize_window()
driver.get('https://5ka.ru/special_offers')

button_location = driver.find_element(By.XPATH, "//button[@class='btn-main focus-btn location-confirm__button red']")
button_location.click()
button_cookies = driver.find_element(By.XPATH, "//button[@class='btn-main focus-btn red small']")
button_cookies.click()

while True:
    wait = WebDriverWait(driver, 15)
    try:
        button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='add-more-btn']")))
        button.click()
    except TimeoutException:
        print("Конец прокрутки.")
        break

goods_list = []
goods = driver.find_elements(By.XPATH, "//div[@class='product-card item']")
for good in goods:
    name = good.find_element(By.XPATH, ".//div[@class='image-cont']/img").get_attribute('alt')
    price = int(good.find_element(By.XPATH, ".//div[@class='prices']/div/span").text.lstrip('от '))
    image = good.find_element(By.XPATH, ".//div[@class='image-cont']/img").get_attribute('src')
    goods_dict = {
        'Наименование товара': name,
        'Цена от': price,
        'Ссылка на изображение': image,
    }
    goods_list.append(goods_dict)

client = MongoClient()
db = client['products']
products_5ka_collection = db['products_5ka']
for good in goods_list:
    products_5ka_collection.insert_one(good)
