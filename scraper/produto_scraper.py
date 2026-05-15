from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import traceback


def converter_preco(valor):
    return float(valor.replace(".", "").replace(",", "."))


def obter_precos(driver, url):

    print(f"🟡 Abrindo produto: {url}")

    driver.get(url)

    print("✅ Página do produto carregada")

    wait = WebDriverWait(driver, 20)

    titulo = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "h1.ui-pdp-title")
        )
    ).text

    print(f"✅ Produto: {titulo}")

    preco_atual_el = wait.until(
        EC.presence_of_element_located(
            (
                By.CSS_SELECTOR,
                ".ui-pdp-price__second-line .andes-money-amount__fraction"
            )
        )
    )

    preco_atual = converter_preco(preco_atual_el.text)

    print(f"💰 Preço atual: {preco_atual}")

    preco_antigo = 0

    try:
        antigo_el = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//s//span[contains(@class,'andes-money-amount__fraction')]"
            ))
        )

        preco_antigo = converter_preco(antigo_el.text)

    except TimeoutException:
        try:
            antigo_el = driver.find_element(
                By.XPATH,
                "//div[contains(@class,'ui-pdp-price__second-line')]//s//span"
            )
            preco_antigo = converter_preco(antigo_el.text)

        except:
            print("⚠️ preço antigo não encontrado no DOM atual")
            preco_antigo = 0

    desconto = 0

    if preco_antigo > 0 and preco_atual < preco_antigo:

        desconto = (
            (preco_antigo - preco_atual)
            / preco_antigo
        ) * 100

        print(f"🔥 Desconto: {round(desconto,1)}%")

    try:

        imagem_element = driver.find_element(
            By.CSS_SELECTOR,
            "img.ui-pdp-gallery__figure__image"
        )

        imagem = (
            imagem_element.get_attribute("data-zoom")
            or imagem_element.get_attribute("src")
        )

        print("✅ Imagem encontrada")

    except:

        imagem = None

        print("⚠️ Imagem não encontrada")

    return {
        "titulo": titulo,
        "atual": preco_atual,
        "antigo": preco_antigo,
        "imagem": imagem,
        "desconto": round(desconto, 1),
        "parcelamento": "Consulte as opções de parcelamento"
    }