from scraper.coletor import coletar_ofertas
from database.db import criar_tabelas
from scraper.produto_scraper import obter_precos
from notificacao.telegram import enviar_mensagem_com_foto
from database.db import (
    conectar,
    pode_enviar,
    registrar_envio,
    produto_ja_enviado,
    registrar_produto_enviado
)
import time


INTERVALO_ENVIO = 120  # 2 minutos

def formatar_br(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def rodar_bot():
    print("Iniciando coleta...")

    db = conectar()

    if not pode_enviar(db):
        print("Limite diário atingido")
        return

    links = coletar_ofertas()

    print(f"{len(links)} links encontrados")

    enviados = 0

    for url in links:

        if enviados >= 10:
            break

        try:

            if produto_ja_enviado(url):
                print("Produto já enviado anteriormente, pulando...")
                continue

            print(f"Analisando: {url}")

            dados = obter_precos(url)

            preco_atual = dados["atual"]
            preco_antigo = dados["antigo"]

            print(f"Atual: {preco_atual}")
            print(f"Antigo: {preco_antigo}")

            if preco_antigo > 0 and preco_atual < preco_antigo:

                print("🔥 PROMOÇÃO ENCONTRADA!")

                enviar_mensagem_com_foto(
                    f"🔥 PROMOÇÃO ENCONTRADA!\n\n"
                    f"<b> {dados['titulo']}</b>\n\n"
                    f"💸 Antes: {formatar_br(preco_antigo)}\n"
                    f"💰 Agora: {formatar_br(preco_atual)}\n"
                    f"📉 Desconto: {dados['desconto']}%\n\n"
                    f"💳 {dados['parcelamento']}\n\n"
                    f"🔗 {url}",
                    dados["imagem"]
                )

                registrar_produto_enviado(url)
                registrar_envio(db)

                enviados += 1

                print("⏳ Aguardando 2 minutos antes do próximo envio...")
                time.sleep(INTERVALO_ENVIO)

        except Exception as e:
            print(f"ERRO: {e}")


criar_tabelas()

while True:
    rodar_bot()
    print("Aguardando 10 segundos...")
    #time.sleep(300) 5 minutos
    time.sleep(10)