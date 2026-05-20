from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def criar_driver():
    options = Options()

    # Oculta a janela se mantido. Caso queira ver o robô navegando na sua tela, comente a linha abaixo!
    #options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=900,900")

    # Otimizações de performance locais
    #options.add_argument("--blink-settings=imagesEnabled=false")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-blink-features=AutomationControlled")

    # O Selenium 4 encontra o Google Chrome instalado no seu Windows automaticamente
    driver = webdriver.Chrome(options=options)
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


def coletar_ofertas(driver):
    print("🟡 Abrindo página de ofertas do Mercado Livre via Selenium")
    driver.get("https://www.mercadolivre.com.br/ofertas")
    print("✅ Página carregada")

    wait = WebDriverWait(driver, 30)
    print("🟡 Aguardando anúncios carregarem na tela...")
    
    # Aguarda até que os links de produtos reais comecem a aparecer no DOM
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/p/']")))
    print("✅ Produtos detectados visualmente")

    time.sleep(3)

    links = []
    # Captura todas as tags de links que apontam para páginas de produtos (/p/)
    elementos = driver.find_elements(By.CSS_SELECTOR, "a[href*='/p/']")
    print(f"🟡 {len(elementos)} elementos de anúncio mapeados")

    for el in elementos:
        try:
            href = el.get_attribute("href")
            if href and "mercadolivre.com.br" in href:
                links.append(href)
        except Exception:
            pass

    # Remove duplicatas mantendo a integridade da lista
    links = list(set(links))
    print(f"✅ {len(links)} links de produtos limpos e unificados.")

    # Retorna os 10 primeiros para evitar sobrecarga no ciclo
    return links[:10]