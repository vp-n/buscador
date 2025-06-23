from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse

def extrair_carros_completos_facebook(html):
    soup = BeautifulSoup(html, "html.parser")
    cards = soup.find_all("a", href=True)

    carros = []

    for card in cards:
        try:
            href = card.get("href", "")
            if "/marketplace/item/" not in href:
                continue

            link = "https://www.facebook.com" + href

            img_tag = card.find("img", alt=True)
            alt = img_tag["alt"].strip() if img_tag else ""
            imagem = img_tag["src"] if img_tag else None

            texto_card = card.get_text(separator=" ", strip=True)

            # Ano
            ano_match = re.search(r"\b(19|20)\d{2}\b", alt)
            ano = ano_match.group(0) if ano_match else None

            # Marca e modelo
            partes = alt.split()
            marca = partes[1].upper() if len(partes) > 1 else None
            modelo = " ".join(partes[2:]).split("no grupo")[0].strip().title()

            # Localização
            localizacao_match = re.search(r"no grupo (.*)$", alt)
            localizacao = localizacao_match.group(1).strip() if localizacao_match else None

            # Preço
            preco_match = re.search(r"R\$ ?([\d\.]+)", texto_card)
            preco = float(preco_match.group(1).replace(".", "")) if preco_match else None

            # Quilometragem
            km = None
            spans = card.find_all("span")
            for span in spans:
                texto_span = span.get_text(strip=True).lower()
                if "km" in texto_span:
                    km_match = re.search(r"([\d\.,]+)\s*(mil)?\s*km", texto_span)
                    if km_match:
                        num = km_match.group(1).replace(",", ".").replace(".", "")
                        km = int(float(num) * 1000) if km_match.group(2) else int(num)
                        break

            # Favicon automático
            site_icon = "https://www.google.com/s2/favicons?domain=www.facebook.com&sz=64"

            carros.append({
                "ano": ano,
                "descricao": alt,
                "imagem": imagem,
                "link": link,
                "localizacao": localizacao,
                "marca": marca,
                "modelo": modelo,
                "preco": preco,
                "quilometragem": km,
                "site_icon": site_icon
            })

        except Exception as e:
            print(f"[ERRO] {e}")
            continue

    return carros
