from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time
import json


def criar_driver():
    options = Options()

    options.binary_location = "/usr/bin/chromium"

    # Configurações essenciais para rodar em Docker/Railway
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")  # Força o Chrome a usar a RAM normal (/tmp) em vez de /dev/shm
    options.add_argument("--disable-gpu")

    # Otimizações de performance (reduz consumo)
    options.add_argument("--blink-settings=imagesEnabled=false")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-software-rasterizer")

    # Remove detecção de automação básica (evita bloqueios iniciais)
    options.add_argument("--disable-blink-features=AutomationControlled")

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


def coletar_ofertas(driver):  # <--- Recebe o driver como argumento
    print("🟡 Buscando ofertas via API usando Selenium")
    
    url = "https://api.mercadolibre.com/sites/MLB/search?q=ofertas"
    
    try:
        # O Selenium abre o endpoint da API
        driver.get(url)
        
        # Pega o texto puro que a API retornou na tela
        corpo_pagina = driver.find_element(By.TAG_NAME, "pre").text
        
        # Converte a string de texto para um dicionário Python
        data = json.loads(corpo_pagina)
        
        if "results" not in data:
            print(" 'results' não veio na resposta")
            return []

        links = []
        for item in data["results"][:20]:
            links.append(item["permalink"])

        print(f"✅ {len(links)} links coletados via Selenium/API")
        return links
        
    except Exception as e:
        print("💥 ERRO NA API COM SELENIUM:", e)
        return []