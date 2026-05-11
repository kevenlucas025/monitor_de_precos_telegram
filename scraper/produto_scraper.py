import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def obter_precos(url):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        time.sleep(5)

        html = driver.page_source

        # 🔥 pega todos os preços da página
        precos = re.findall(r"R\$\s?([\d\.\,]+)", html)

        valores = []
        for p in precos:
            try:
                p = float(p.replace(".", "").replace(",", "."))
                valores.append(p)
            except:
                pass

        driver.quit()

        if not valores:
            raise Exception("Nenhum preço encontrado")

        # 🔥 lógica importante:
        preco_atual = min(valores)      # menor = promoção
        preco_antigo = max(valores)     # maior = riscado

        return {
            "atual": preco_atual,
            "antigo": preco_antigo
        }

    finally:
        driver.quit()