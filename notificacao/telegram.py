import requests
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def enviar_mensagem_com_foto(texto, imagem):

    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"

    payload = {
        "chat_id": CHAT_ID,
        "photo": imagem,
        "caption": texto,
        "parse_mode": "HTML"
    }

    response = requests.post(url, data=payload)

    return response.status_code