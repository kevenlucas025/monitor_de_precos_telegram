from scraper.produto_scraper import obter_precos


def analisar_produto(url):
    dados = obter_precos(url)

    preco_atual = dados["atual"]
    preco_antigo = dados["antigo"]

    if preco_atual < preco_antigo:
        return {
            "promo": True,
            "url": url,
            "atual": preco_atual,
            "antigo": preco_antigo
        }

    return {"promo": False}