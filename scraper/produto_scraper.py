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

    # ----------------------------
    # TÍTULO (COM FALLBACK)
    # ----------------------------
    titulo = None

    seletores_titulo = [
        "h1.ui-pdp-title",
        "h1",
        "h1 span"
    ]

    
    for sel in seletores_titulo:
        try:
            elemento = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, sel))
            )

            titulo = elemento.text.strip()

            if titulo:
                break

        except TimeoutException:
            continue

        except Exception:
            continue

    if not titulo:
        raise Exception("❌ Título não encontrado")

    print(f"✅ Produto: {titulo}")

    # ----------------------------
    # PREÇO ATUAL
    # ----------------------------
    preco_atual_el = None

    seletores_preco = [
        ".ui-pdp-price__second-line .andes-money-amount__fraction",
        ".andes-money-amount__fraction"
    ]

    for sel in seletores_preco:
        try:
            preco_atual_el = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, sel))
            )
            if preco_atual_el:
                break
        except TimeoutException:
            continue

    if not preco_atual_el:
        raise Exception("❌ Preço atual não encontrado")

    preco_atual = converter_preco(preco_atual_el.text)

    print(f"💰 Preço atual: {preco_atual}")

    # ----------------------------
    # PREÇO ANTIGO
    # ----------------------------
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

    # ----------------------------
    # DESCONTO
    # ----------------------------
    desconto = 0

    if preco_antigo > 0 and preco_atual < preco_antigo:
        desconto = ((preco_antigo - preco_atual) / preco_antigo) * 100
        print(f"🔥 Desconto: {round(desconto, 1)}%")

    # ----------------------------
    # IMAGEM
    # ----------------------------
    # ----------------------------
    imagem = None

    try:
        imagem_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "img.ui-pdp-image")
            )
        )

        atributos = [
            "data-zoom",
            "data-src",
            "src",
        ]

        for attr in atributos:
            valor = imagem_element.get_attribute(attr)

            if valor and valor.startswith("http"):
                imagem = valor
                break

        print(f"🖼️ IMAGEM CAPTURADA: {imagem}")

    except Exception as e:
        print(f"⚠️ Erro ao capturar imagem: {e}")

    # ----------------------------
    # RETURN
    # ----------------------------
    return {
        "titulo": titulo,
        "atual": preco_atual,
        "antigo": preco_antigo,
        "imagem": imagem,
        "desconto": round(desconto, 1),
        "parcelamento": "Consulte as opções de parcelamento"
    }