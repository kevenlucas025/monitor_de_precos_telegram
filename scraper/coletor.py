from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import traceback
import time


def criar_driver():
    options = Options()

    # 🔥 modo produção (Railway)
    options.add_argument("--headless=new")  # obrigatório no Railway
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    # estabilidade Chrome em container
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-background-networking")
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-renderer-backgrounding")
    options.add_argument("--disable-features=TranslateUI")

    driver = webdriver.Chrome(options=options)

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


def coletar_ofertas(driver):

    print("🟡 Abrindo Mercado Livre ofertas")

    driver.get("https://www.mercadolivre.com.br/ofertas")

    print("✅ Página carregada")

    wait = WebDriverWait(driver, 30)

    print("🟡 Aguardando produtos aparecerem")

    wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "a[href*='/p/']")
        )
    )

    print("✅ Produtos encontrados na página")

    time.sleep(3)

    links = []

    elementos = driver.find_elements(
        By.CSS_SELECTOR,
        "a[href*='/p/']"
    )

    print(f"🟡 {len(elementos)} elementos encontrados")

    for el in elementos:

        try:

            href = el.get_attribute("href")

            if href and "mercadolivre.com.br" in href:
                links.append(href)

        except Exception:
            print("⚠️ erro lendo elemento")

    links = list(set(links))

    print(f"✅ {len(links)} links coletados")

    return links[:10]   