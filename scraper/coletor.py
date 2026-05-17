from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time
import os
import json
import urllib.request
import urllib.parse
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("ML_CLIENT_ID")
CLIENT_SECRET = os.getenv("ML_CLIENT_SECRET")

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

    driver.get("https://www.mercadolivre.com.br/afiliados/linkbuilder#hub")
    print("✅ Link builder carregado")

    textarea = wait.until(EC.element_to_be_clickable((By.ID, "url-0")))
    print("✅ Campo encontrado")

    url_produto = url_produto.split("#")[0]
    textarea.clear()
    textarea.send_keys(url_produto)
    print("✅ URL preenchida")

    gerar_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Gerar')]")))
    print("✅ Botão gerar encontrado")
    gerar_btn.click()
    print("✅ Botão clicado")

    time.sleep(5)
    return True


def copiar_link_curto(driver):
    print("🟡 Copiando link curto")
    wait = WebDriverWait(driver, 30)
    campo = wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[contains(@id,'textfield-copyLink')]")))
    print("✅ Link curto encontrado")
    return campo.get_attribute("value")


def obter_acesso_token():
    url = "https://api.mercadolibre.com/oauth/token"
    
    payload = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    
    # Transforma o dicionário no formato x-www-form-urlencoded exigido pela API
    data = urllib.parse.urlencode(payload).encode("utf-8")
    
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Accept", "application/json")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                res_data = json.loads(response.read().decode("utf-8"))
                return res_data.get("access_token")
            else:
                print(f"❌ Erro ao gerar token oficial: {response.status}")
                return None
    except Exception as e:
        print(f"💥 Falha na autenticação com o Mercado Livre: {e}")
        return None


def coletar_ofertas():
    print("🟡 Buscando ofertas via API Oficial do Mercado Livre")
    
    token = obter_acesso_token()
    if not token:
        print("❌ Coleta abortada: Não foi possível obter o Access Token.")
        return []

    url = "https://api.mercadolibre.com/sites/MLB/search?q=ofertas"
    
    req = urllib.request.Request(url, method="GET")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/json")
    
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            if response.status != 200:
                print(f"❌ Erro na API. Status: {response.status}")
                return []
                
            data = json.loads(response.read().decode("utf-8"))
            
            if "results" not in data:
                print("❌ Estrutura 'results' não foi encontrada no JSON")
                return []
            
            links = []
            for item in data['results'][:20]:
                if "permalink" in item:
                    links.append(item["permalink"])

            print(f"✅ {len(links)} links coletados com sucesso e de forma oficial!")
            return links
            
    except Exception as e:
        print("💥 ERRO CRÍTICO NA REQUISIÇÃO DA API:", e)
        return []