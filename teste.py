from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

options = Options()

options.add_argument(
    r"--user-data-dir=C:\Users\KevenJesus\AppData\Local\Google\Chrome\UserData"
)

options.add_argument("--profile-directory=Default")

driver = webdriver.Chrome(options=options)

driver.get("https://www.mercadolivre.com.br")

time.sleep(9999)