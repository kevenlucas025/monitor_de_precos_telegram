from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def coletar_ofertas():

    options = Options()

    # para debug deixe visível
    options.add_argument("--headless=new")

    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0")

    driver = webdriver.Chrome(options=options)

    try:

        url = "https://www.mercadolivre.com.br/ofertas"

        print("Abrindo Mercado Livre...")

        driver.get(url)

        wait = WebDriverWait(driver, 20)

        # espera os cards aparecerem
        wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "a")
            )
        )

        print("Página carregada!")

        links = []

        elementos = driver.find_elements(By.TAG_NAME, "a")

        for el in elementos:

            href = el.get_attribute("href")

            if href:

                # links reais de produtos
                if "mercadolivre.com.br/" in href and "/p/" in href:

                    links.append(href)

        links = list(set(links))

        print(f"{len(links)} links coletados")

        return links

    finally:
        driver.quit()