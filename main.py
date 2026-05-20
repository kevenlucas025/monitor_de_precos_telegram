from scraper.coletor import (
    criar_driver,
    coletar_ofertas,
    gerar_link_afiliado,
    copiar_link_curto
)

from scraper.produto_scraper import obter_precos
from notificacao.telegram import enviar_mensagem_com_foto
from scraper.cookies import carregar_cookies
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

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)
# =========================
# LOOP PRINCIPAL
# =========================
def rodar_bot():
    log("=== INICIANDO CICLO ===")

    db = conectar()

    if not pode_enviar(db):
        log("⛔ Limite diário atingido")
        return

    driver = None

    try:
        # 1️⃣ PRIMEIRO: Instancia o navegador local, pois precisamos dele para a raspagem das ofertas
        log("🟡 Criando driver para iniciar ciclo...")
        driver = criar_driver()
        
        if driver is None:
            log("❌ Falha crítica: O driver não pôde ser criado.")
            return
            
        carregar_cookies(driver)
        log("✅ Driver criado com sucesso")

        # 2️⃣ SEGUNDO: Raspa a página de ofertas passando o navegador como ferramenta
        log("🟡 Coletando ofertas...")
        links = coletar_ofertas(driver)

        # Filtra para descobrir itens inéditos
        novos_links = [url for url in links if url not in links_processados]
        log(f"🔎 {len(novos_links)} produtos novos encontrados")

        # 3️⃣ TERCEIRO: Loop de processamento de promoções
        if novos_links:
            for i, url in enumerate(novos_links):
                log(f"\n📦 [{i+1}/{len(novos_links)}] Analisando produto")
                log(f"🔗 {url}")

                links_processados.add(url)

                try:
                    if produto_ja_enviado(url):
                        log("⚠️ Já enviado, pulando")
                        continue

                    log("🟡 Abrindo página do produto...")
                    dados = obter_precos(driver, url)

                    log(f"💰 Preço atual: {dados['atual']}")
                    log(f"🏷️ Preço antigo: {dados['antigo']}")

                    if not (dados["antigo"] > 0 and dados["atual"] < dados["antigo"]):
                        log("❌ Sem promoção detectada")
                        continue

                    log("🔥 PROMOÇÃO ENCONTRADA")

                    gerar_link_afiliado(driver, url)
                    link_curto = copiar_link_curto(driver) or url

                    log("📤 Enviando Telegram...")

                    enviar_mensagem_com_foto(
                        f"🔥 PROMOÇÃO ENCONTRADA!\n\n"
                        f"<b>{dados['titulo']}</b>\n\n"
                        f"💸 Antes: {formatar_br(dados['antigo'])}\n"
                        f"💰 Agora: {formatar_br(dados['atual'])}\n"
                        f"📉 Desconto: {dados['desconto']}%\n\n"
                        f"💳 {dados['parcelamento']}\n\n"
                        f"🔗 {link_curto}",
                        dados["imagem"]
                    )

                    registrar_envio(db)
                    registrar_produto_enviado(url)

                    log("✅ Enviado com sucesso")
                    log("⏳ Aguardando 2 minutos...")
                    time.sleep(INTERVALO_ENVIO)

                except Exception:
                    import traceback
                    log("💥 ERRO AO PROCESSAR PRODUTO")
                    print(traceback.format_exc())
        else:
            log("⏳ Sem novidades neste ciclo.")

    except Exception as e:
        log(f"💥 ERRO CRÍTICO NO CICLO: {e}")
        import traceback
        print(traceback.format_exc())

    finally:
        # Garante o encerramento da sessão do navegador local ao fim do ciclo
        if driver is not None:
            log("🧹 Fechando driver")
            try:
                driver.quit()
            except:
                pass

# =========================
# LOOP INFINITO
# =========================
def main():
    criar_tabelas()

    log("APP INICIOU")

    while True:
        try:
            log("🔥 NOVO CICLO INICIADO")
            rodar_bot()

        except Exception as e:
            log(f"💥 ERRO NO LOOP: {e}")

        time.sleep(10)


if __name__ == "__main__":
    main()