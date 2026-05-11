from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time


def coletar_ofertas():
    options = Options()
    options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=options)

    driver.get("https://www.mercadolivre.com.br/ofertas")

    time.sleep(5)

    links = []

    elementos = driver.find_elements(By.TAG_NAME, "a")

    for el in elementos:
        href = el.get_attribute("href")
        if href and "/p/" in href:
            links.append(href)

    driver.quit()

    return list(set(links))