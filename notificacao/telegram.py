import requests
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def enviar_mensagem_com_foto(texto, imagem):
    
    if imagem:
        url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
        payload = {
            "chat_id": CHAT_ID,
            "photo": imagem,
            "caption": texto,
            "parse_mode": "HTML"
        }
    else:
        print(f"🖼️ URL imagem capturada: {imagem}")
        print("Produto sem foto detectado. Enviando apenas texto...")
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": texto,
            "parse_mode": "HTML"
        }

    try:
        # Usar json=payload ou data=payload (para sendMessage o json= é mais seguro)
        response = requests.post(url, data=payload, timeout=15)
        print("🤖 RESPOSTA DO TELEGRAM:", response.status_code, response.text)
        return response.status_code
    
    except Exception as e:
        print(f"💥 Erro de rede ao falar com o Telegram: {e}")
        return 500