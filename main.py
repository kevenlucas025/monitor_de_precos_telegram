from scraper.coletor import (
    criar_driver,
    coletar_ofertas,
    gerar_link_afiliado,
    copiar_link_curto
)

from scraper.produto_scraper import obter_precos
from notificacao.telegram import enviar_mensagem_com_foto
from database.db import (
    conectar,
    pode_enviar,
    registrar_envio,
    produto_ja_enviado,
    registrar_produto_enviado,
    criar_tabelas
)

import time

links_processados = set()
INTERVALO_ENVIO = 120


def formatar_br(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


# =========================
# LOOP PRINCIPAL
# =========================
def rodar_bot():

    print("\n=== INICIANDO CICLO ===")

    db = conectar()

    if not pode_enviar(db):
        print("Limite diário atingido")
        return

    driver = criar_driver()

    try:

        links = coletar_ofertas(driver)

        novos_links = [url for url in links if url not in links_processados]

        print(f"{len(novos_links)} produtos novos encontrados")

        for url in novos_links:

            links_processados.add(url)

            try:

                if produto_ja_enviado(url):
                    print("Já enviado, pulando...")
                    continue

                print("\nAnalisando:", url)

                dados = obter_precos(driver,url)

                preco_atual = dados["atual"]
                preco_antigo = dados["antigo"]

                if not (preco_antigo > 0 and preco_atual < preco_antigo):
                    print("Sem promoção")
                    continue

                print("🔥 PROMOÇÃO ENCONTRADA")

                # gera link afiliado
                gerar_link_afiliado(driver, url)

                # pega link curto
                link_curto = copiar_link_curto(driver)

                if not link_curto:
                    print("Falha ao copiar link, usando fallback")
                    link_curto = url

                # envia telegram
                enviar_mensagem_com_foto(
                    f"🔥 PROMOÇÃO ENCONTRADA!\n\n"
                    f"<b>{dados['titulo']}</b>\n\n"
                    f"💸 Antes: {formatar_br(preco_antigo)}\n"
                    f"💰 Agora: {formatar_br(preco_atual)}\n"
                    f"📉 Desconto: {dados['desconto']}%\n\n"
                    f"💳 {dados['parcelamento']}\n\n"
                    f"🔗 Link: {link_curto}",
                    dados["imagem"]
                )

                registrar_envio(db)
                registrar_produto_enviado(url)

                print("Enviado com sucesso")

                # delay entre envios (CORRETO)
                print("Aguardando 2 minutos antes do próximo envio...\n")
                time.sleep(INTERVALO_ENVIO)

            except Exception:
                import traceback
                print("ERRO COMPLETO:")
                print(traceback.format_exc())

    finally:
        driver.quit()


# =========================
# LOOP INFINITO
# =========================
def main():
    criar_tabelas()

    print("APP INICIOU")

    while True:
        try:
            print("🔥 NOVO CICLO")
            rodar_bot()

        except Exception as e:
            print("💥 ERRO NO LOOP:", e)

        time.sleep(10)


if __name__ == "__main__":
    main()