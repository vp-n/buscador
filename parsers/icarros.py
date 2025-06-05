from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re

def identificar_favicon(link):
    dominio = urlparse(link).hostname or "www.icarros.com.br"
    return f"https://www.google.com/s2/favicons?domain={dominio}&sz=64"

def extrair_carros_completos_icarros(html):
    soup = BeautifulSoup(html, "html.parser")
    cards = soup.select("li.small-offer-card")
    carros = []
    chaves_vistas = set()

    for card in cards:
        try:
            # Link
            a_tag = card.find("a", href=True)
            link = a_tag["href"] if a_tag else None
            if link and not link.startswith("http"):
                link = f"https://www.icarros.com.br{link}"

            if not link:
                continue

            # Imagem
            img_tag = card.find("img")
            imagem = img_tag["src"].strip() if img_tag and img_tag.get("src") else None

            # Descrição
            descricao_tag = card.select_one(
                "div.small-offer-card__header a p.label__neutral.ids_textStyle_label_xsmall_regular")
            descricao = descricao_tag.text.strip() if descricao_tag else None

            # Combustível e câmbio
            combustivel = cambio = None
            if descricao:
                combustiveis = ["Flex", "Gasolina", "Etanol", "Diesel", "Elétrico", "Híbrido"]
                for tipo in combustiveis:
                    if tipo.lower() in descricao.lower():
                        combustivel = tipo
                        break
                if "manual" in descricao.lower():
                    cambio = "Manual"
                elif "automático" in descricao.lower() or "automatico" in descricao.lower():
                    cambio = "Automático"

            # Preço
            preco_tag = card.select_one("div.small-offer-card__price-container p.label__onLight.ids_textStyle_label_medium_bold")
            preco = None
            if preco_tag:
                texto = preco_tag.text.strip().replace("R$", "").replace(".", "").replace(",", ".")
                try:
                    preco = float(texto)
                except ValueError:
                    pass

            # Ano
            ano_tag = card.select_one("div.info-container__car-info p.label__neutral-variant.ids_textStyle_label_xsmall_regular")
            ano = ano_tag.text.strip() if ano_tag else None

            # Quilometragem
            km_tag = card.select_one("div.info-container__car-info p.label__neutral.ids_textStyle_label_xsmall_regular")
            quilometragem = None
            if km_tag:
                texto = km_tag.text.strip().lower().replace("km", "").replace(".", "").strip()
                try:
                    quilometragem = int(texto)
                except ValueError:
                    pass

            # Localização
            loc_tag = card.select_one("div.info-container__location-info p.label__neutral.ids_textStyle_label_xsmall_regular")
            localizacao = loc_tag.text.strip() if loc_tag else None

            # Marca: extraída do link
            marca = None
            match = re.search(r"icarros\.com\.br/comprar/[^/]+/([^/]+)/", link)
            if match:
                marca = match.group(1).capitalize()

            # Modelo resumido da descrição
            modelo = None
            if descricao:
                # Regex para pegar até "1.0 8V", "1.6 16V", etc.
                match = re.search(r"^.*?\d\.\d(?:\s*\d{0,2}V)?", descricao)
                modelo = match.group().strip() if match else descricao

            # Verifica duplicidade por chave única
            chave = f"{marca}|{modelo}|{ano}|{quilometragem}"
            if chave in chaves_vistas:
                continue
            chaves_vistas.add(chave)

            carros.append({
                "marca": marca,
                "modelo": modelo,
                "preco": preco,
                "ano": ano,
                "quilometragem": quilometragem,
                "combustivel": combustivel,
                "cambio": cambio,
                "localizacao": localizacao,
                "descricao": descricao,
                "imagem": imagem,
                "link": link,
                "site_icon": identificar_favicon(link)
            })

        except Exception as e:
            print(f"[ERRO] Falha ao processar card: {e}")
            continue

    return carros