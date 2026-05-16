from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time
import requests


def criar_driver():
    options = Options()

    options.binary_location = "/usr/bin/chromium"

    # ESSENCIAL
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # 🔥 EVITA CRASH
    options.add_argument("--disable-gpu")
    options.add_argument("--single-process")
    options.add_argument("--no-zygote")
    options.add_argument("--disable-software-rasterizer")

    # 🔥 REDUZ USO
    options.add_argument("--blink-settings=imagesEnabled=false")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")

    service = Service("/usr/bin/chromedriver")

    driver = webdriver.Chrome(service=service, options=options)

    return driver


def gerar_link_afiliado(driver, url_produto):

    print("🟡 Abrindo link builder")

    wait = WebDriverWait(driver, 30)

    driver.get(
        "https://www.mercadolivre.com.br/afiliados/linkbuilder#hub"
    )

    print("✅ Link builder carregado")

    textarea = wait.until(
        EC.element_to_be_clickable((By.ID, "url-0"))
    )

    print("✅ Campo encontrado")

    url_produto = url_produto.split("#")[0]

    textarea.clear()
    textarea.send_keys(url_produto)

    print("✅ URL preenchida")

    gerar_btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(., 'Gerar')]")
        )
    )

    print("✅ Botão gerar encontrado")

    gerar_btn.click()

    print("✅ Botão clicado")

    time.sleep(5)

    return True


def copiar_link_curto(driver):

    print("🟡 Copiando link curto")

    wait = WebDriverWait(driver, 30)

    campo = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//textarea[contains(@id,'textfield-copyLink')]")
        )
    )

    print("✅ Link curto encontrado")

    return campo.get_attribute("value")


def coletar_ofertas():

    print("🟡 Buscando ofertas via API")

    url = "https://api.mercadolibre.com/sites/MLB/search?q=ofertas"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    res = requests.get(url, headers=headers)
    data = res.json()

    links = []

    for item in data["results"][:20]:
        links.append(item["permalink"])

    print(f"✅ {len(links)} links coletados via API")

    return links