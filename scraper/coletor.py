import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import pyperclip


# =========================
# DRIVER ÚNICO (IMPORTANTE)
# =========================
def criar_driver():

    options = uc.ChromeOptions()

    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(r"--user-data-dir=C:\bot_chrome")
    options.add_argument("--no-sandbox")
    options.add_argument("--start-maximized")

    driver = uc.Chrome(
        options=options,
        use_subprocess=True
    )

    return driver


# =========================
# GERAR LINK AFILIADO
# =========================
def gerar_link_afiliado(driver, url_produto):

    wait = WebDriverWait(driver, 30)

    print("Abrindo link builder...")

    driver.get(
        "https://www.mercadolivre.com.br/afiliados/linkbuilder#hub"
    )

    textarea = wait.until(
        EC.element_to_be_clickable((By.ID, "url-0"))
    )

    url_produto = url_produto.split("#")[0]

    textarea.click()
    textarea.send_keys(Keys.CONTROL, "a")
    textarea.send_keys(Keys.DELETE)
    textarea.send_keys(url_produto)

    print("URL enviada")

    gerar_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Gerar')]"))
    )

    gerar_btn.click()

    print("Gerando link...")

    time.sleep(5)

    print("Aguardando resultado do link...")

    wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//textarea[contains(@id,'textfield-copyLink')]")
        )
    )

    print("Link gerado com sucesso")

    time.sleep(2)

    # pega link afiliado
    textareas = driver.find_elements(By.TAG_NAME, "textarea")

    for ta in textareas:

        val = ta.get_attribute("value")

        if val and "http" in val:

            print("Link afiliado gerado:")
            print(val)

            return val

    return None


# =========================
# CLICAR BOTÃO COPIAR LINK
# =========================
def copiar_link_curto(driver):

    wait = WebDriverWait(driver, 30)

    print("Buscando link no textarea...")

    # pega o textarea que contém o link encurtado
    campo = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//textarea[contains(@id,'textfield-copyLink')]")
        )
    )

    # garante que o valor já está preenchido
    wait.until(lambda d: campo.get_attribute("value") != "")

    link = campo.get_attribute("value")

    print("Link capturado:", link)

    return link


# =========================
# COLETAR OFERTAS
# =========================
def coletar_ofertas(driver):

    print("Abrindo Mercado Livre...")

    driver.get("https://www.mercadolivre.com.br/ofertas")

    wait = WebDriverWait(driver, 20)

    wait.until(
        EC.presence_of_element_located((By.TAG_NAME, "a"))
    )

    time.sleep(5)

    links = []

    elementos = driver.find_elements(By.TAG_NAME, "a")

    for el in elementos:

        href = el.get_attribute("href")

        if href:

            if (
                "mercadolivre.com.br/" in href
                and "/p/" in href
            ):
                links.append(href)

    links = list(set(links))

    print(f"{len(links)} links coletados")

    return links[:10]