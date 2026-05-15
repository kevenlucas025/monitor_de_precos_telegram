import json
import os

COOKIES_FILE = "cookies_ml.json"


def salvar_cookies(driver):
    cookies = driver.get_cookies()

    with open(COOKIES_FILE, "w") as f:
        json.dump(cookies, f)


def carregar_cookies(driver):
    if not os.path.exists(COOKIES_FILE):
        print("⚠️ Cookies não encontrados")
        return False

    driver.get("https://www.mercadolivre.com.br")

    with open(COOKIES_FILE, "r", encoding="utf-8") as f:
        cookies = json.load(f)

    for cookie in cookies:
        cookie.pop("sameSite", None)
        cookie.pop("domain", None)  # 👈 importante no Railway
        try:
            driver.add_cookie(cookie)
        except:
            pass

    driver.refresh()

    print("✅ Cookies carregados")
    return True