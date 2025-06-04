import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def identificar_favicon(link):
    dominio = urlparse(link).hostname or ""
    return f"https://www.google.com/s2/favicons?domain={dominio}&sz=64"

def extrair_carros_completos_olx(html):
    soup = BeautifulSoup(html, "html.parser")
    cards = soup.find_all("section", class_="olx-adcard")
    carros = []

    for card in cards:
        try:
            a_tag = card.find("a", class_="olx-adcard__link")
            titulo = a_tag.get("title", "") if a_tag else ""
            link = a_tag.get("href", "") if a_tag else ""

            preco_tag = card.find("h3", class_=re.compile("olx-adcard__price"))
            preco_match = re.search(r"R\$ ?([\d\.]+)", preco_tag.text) if preco_tag else None
            preco = int(preco_match.group(1).replace('.', '')) if preco_match else None

            km_tag = card.find("div", class_="olx-adcard__detail")
            km_match = re.search(r"([\d\.]+)\s?km", km_tag.text) if km_tag else None
            km = int(km_match.group(1).replace('.', '')) if km_match else None

            img_tag = card.find("img")
            imagem = img_tag.get("src") if img_tag and img_tag.get("src") else None

            local_div = card.find("div", class_="olx-adcard__location-date")
            localizacao = local_div.text.strip() if local_div else None

            partes = titulo.split()
            modelo = f"{partes[0]} {partes[1]}" if len(partes) > 1 else partes[0] if partes else None

            carros.append({
                "modelo": modelo,
                "preco": preco,
                "localizacao": localizacao,
                "quilometragem": km,
                "imagem": imagem,
                "descricao": titulo,
                "link": link,
                "site_icon": identificar_favicon(link)
            })

        except Exception:
            continue

    return carros