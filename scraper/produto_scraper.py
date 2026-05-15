from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def converter_preco(valor):
    return float(valor.replace(".", "").replace(",", "."))


def obter_precos(driver, url):

    driver.get(url)

    wait = WebDriverWait(driver, 20)

    titulo = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "h1.ui-pdp-title")
        )
    ).text

    preco_atual_el = wait.until(
        EC.presence_of_element_located(
            (
                By.CSS_SELECTOR,
                ".ui-pdp-price__second-line .andes-money-amount__fraction"
            )
        )
    )

    preco_atual = converter_preco(preco_atual_el.text)

    preco_antigo = 0

    try:
        antigo_el = driver.find_element(
            By.CSS_SELECTOR,
            ".ui-pdp-price__original-value s .andes-money-amount__fraction"
        )

        preco_antigo = converter_preco(antigo_el.text)

    except:
        try:
            antigo_el = driver.find_element(
                By.CSS_SELECTOR,
                "s .andes-money-amount__fraction"
            )

            preco_antigo = converter_preco(antigo_el.text)

        except:
            preco_antigo = 0

    desconto = 0

    if preco_antigo > 0 and preco_atual < preco_antigo:
        desconto = (
            (preco_antigo - preco_atual)
            / preco_antigo
        ) * 100

    try:

        imagem_element = driver.find_element(
            By.CSS_SELECTOR,
            "img.ui-pdp-gallery__figure__image"
        )

        imagem = (
            imagem_element.get_attribute("data-zoom")
            or imagem_element.get_attribute("src")
        )

    except:
        imagem = None

    return {
        "titulo": titulo,
        "atual": preco_atual,
        "antigo": preco_antigo,
        "imagem": imagem,
        "desconto": round(desconto, 1),
        "parcelamento": "Consulte as opções de parcelamento"
    }