from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time
import json
from curl_cffi import requests


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


def coletar_ofertas():  # <--- Removeu o (driver)
    print("🟡 Buscando ofertas via API camuflada (curl_cffi)")
    
    url = "https://api.mercadolibre.com/sites/MLB/search?q=ofertas"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }
    
    try:
        # O impersonate="chrome" faz a mágica de simular a assinatura TLS do Chrome real
        res = requests.get(url, headers=headers, impersonate="chrome124")
        
        if res.status_code != 200:
            print(f"❌ Erro na API. Status: {res.status_code}")
            return []
            
        data = res.json()
        
        if "results" not in data:
            print("❌ 'results' não veio na resposta da API")
            return []

        links = []
        for item in data["results"][:20]:
            links.append(item["permalink"])

        print(f"✅ {len(links)} links coletados com sucesso via API!")
        return links
        
    except Exception as e:
        print("💥 ERRO CRÍTICO NA COLETA DA API:", e)
        return []