from scraper.coletor import criar_driver
from scraper.cookies import salvar_cookies
import time

driver = criar_driver()

driver.get("https://www.mercadolivre.com.br")

print("👉 FAÇA LOGIN MANUAL AGORA")
time.sleep(60)  # tempo pra logar

# 🔥 aqui salva depois do login
salvar_cookies(driver)

print("✅ Cookies salvos com sucesso")

driver.quit()