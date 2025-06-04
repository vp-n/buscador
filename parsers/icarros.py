import re
import json
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def identificar_favicon(link):
    dominio = urlparse(link).hostname or ""
    return f"https://www.google.com/s2/favicons?domain={dominio}&sz=64"

def extrair_carros_completos_icarros(html):
    soup = BeautifulSoup(html, "html.parser")
    links = soup.select("a.offer-card__title-container")
    carros = []

    for a in links:
        try:
            href = a.get("href", "")
            link = f"https://www.icarros.com.br{href}" if href.startswith("/") else href

            onclick = a.get("onclick", "")
            json_like = re.search(r"\{event: 'select_item', text:.*?\}\s*\)\s*\}\)", onclick, re.DOTALL)
            if not json_like:
                continue

            dados_raw = json_like.group()
            dados_raw = dados_raw.replace("event: 'select_item', ", "")
            dados_raw = re.sub(r"(\w+):", r'"\1":', dados_raw)
            dados_raw = dados_raw.replace("'", '"')
            dados_json = json.loads(dados_raw)

            item = dados_json.get("select_item_items", dados_json.get("select_item", {}))

            modelo = item.get("item_name")
            preco = item.get("price")
            localizacao = item.get("item_category4")
            km = item.get("item_category")
            combustivel = item.get("item_category2")

            # Procura imagem dentro do mesmo card (ancestral de <a>)
            card = a.find_parent("li") or a.find_parent("div")
            img_tag = card.find("img") if card else None
            imagem = img_tag.get("src") if img_tag and img_tag.get("src") else None

            partes_modelo = modelo.split() if modelo else []
            marca = partes_modelo[0] if partes_modelo else None

            carros.append({
                "marca": marca,
                "modelo": modelo,
                "preco": preco,
                "localizacao": localizacao,
                "quilometragem": km,
                "combustivel": combustivel,
                "imagem": imagem,
                "descricao": modelo,
                "link": link,
                "site_icon": identificar_favicon(link)
            })

        except Exception as e:
            print("Erro ao processar anúncio:", e)
            continue

    return carros