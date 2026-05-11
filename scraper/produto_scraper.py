from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def converter_preco(valor):
    return float(valor.replace(".", "").replace(",", "."))


def obter_precos(url):

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        wait = WebDriverWait(driver, 15)

        # título
        titulo = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1.ui-pdp-title"))
        ).text

        # preço atual
        preco_atual_el = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".andes-money-amount__fraction"))
        )

        # preço antigo
        try:
            preco_antigo_el = driver.find_element(
                By.CSS_SELECTOR,
                "s .andes-money-amount__fraction"
            )
            preco_antigo = converter_preco(preco_antigo_el.text)
        except:
            preco_antigo = 0

        preco_atual = converter_preco(preco_atual_el.text)

        # desconto seguro
        desconto = 0
        if preco_antigo > 0:
            desconto = ((preco_antigo - preco_atual) / preco_antigo) * 100

        # imagem (sempre tenta pegar)
        try:
            imagem_element = driver.find_element(
                By.CSS_SELECTOR,
                "img.ui-pdp-gallery__figure__image"
            )

            imagem = imagem_element.get_attribute("data-zoom") or imagem_element.get_attribute("src")

        except:
            imagem = None

        # parcelamento seguro
        try:
            parcelamento = driver.find_element(
                By.CSS_SELECTOR,
                ".ui-pdp-installments"
            ).text
        except:
            parcelamento = None

        return {
            "titulo": titulo,
            "atual": preco_atual,
            "antigo": preco_antigo,
            "imagem": imagem,
            "desconto": round(desconto, 1),
            "parcelamento": parcelamento
        }

    finally:
        driver.quit()