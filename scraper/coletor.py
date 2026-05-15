from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def criar_driver():

    options = Options()

    options.binary_location = "/usr/bin/chromium"

    # obrigatório em container
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # estabilidade
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    # evita crash no render
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-setuid-sandbox")

    # anti travamento
    options.add_argument("--remote-debugging-port=9222")

    driver = webdriver.Chrome(options=options)

    return driver


def gerar_link_afiliado(driver, url_produto):

    wait = WebDriverWait(driver, 30)

    print("Abrindo link builder....")

    driver.get(
        "https://www.mercadolivre.com.br/afiliados/linkbuilder#hub"
    )

    textarea = wait.until(
        EC.element_to_be_clickable((By.ID, "url-0"))
    )

    url_produto = url_produto.split("#")[0]

    textarea.clear()
    textarea.send_keys(url_produto)

    gerar_btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(., 'Gerar')]")
        )
    )

    gerar_btn.click()

    time.sleep(5)

    return True


def copiar_link_curto(driver):

    wait = WebDriverWait(driver, 30)

    campo = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//textarea[contains(@id,'textfield-copyLink')]")
        )
    )

    return campo.get_attribute("value")


def coletar_ofertas(driver):

    print("Abrindo Mercado Livre...")

    driver.get("https://www.mercadolivre.com.br/ofertas")

    wait = WebDriverWait(driver, 20)

    # 🔥 espera links reais de produto aparecerem
    wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "a[href*='/p/']")
        )
    )

    time.sleep(3)

    links = []

    elementos = driver.find_elements(By.CSS_SELECTOR, "a[href*='/p/']")

    for el in elementos:
        href = el.get_attribute("href")

        if href and "mercadolivre.com.br" in href:
            links.append(href)

    links = list(set(links))

    print(f"{len(links)} links coletados")

    return links[:10]