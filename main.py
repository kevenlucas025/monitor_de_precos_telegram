from scraper.coletor import coletar_ofertas
from scraper.produto_scraper import obter_precos
from notificacao.telegram import enviar_mensagem
from database.db import conectar,pode_enviar,registrar_envio
import time


def rodar_bot():
    db = conectar()

    if not pode_enviar(db):
        print("Limite diário atingido")
        return

    links = coletar_ofertas()

    enviados = 0

    for url in links:

        if enviados >= 10:
            break

        try:
            dados = obter_precos(url)

            preco_atual = dados["atual"]
            preco_antigo = dados["antigo"]

            if preco_atual < preco_antigo:

                enviar_mensagem(
                    f"🔥 PROMOÇÃO!\n\n"
                    f"💸 Antes: R$ {preco_antigo}\n"
                    f"💰 Agora: R$ {preco_atual}\n"
                    f"🔗 {url}"
                )

                registrar_envio(db)
                enviados += 1

        except:
            continue


while True:
    rodar_bot()
    time.sleep(300)