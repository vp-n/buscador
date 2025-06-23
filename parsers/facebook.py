from bs4 import BeautifulSoup
import re


def extrair_carros_completos_facebook(html):
    soup = BeautifulSoup(html, "html.parser")

    # Achar todos os links que contêm /marketplace/item/
    todos_links = soup.find_all("a", href=True)
    carros = []

    for card in todos_links:
        try:
            href = card.get("href", "")
            if "/marketplace/item/" not in href:
                continue

            link = "https://www.facebook.com" + href

            # Procura a imagem (se tiver)
            img_tag = card.find("img", alt=True)
            alt = img_tag["alt"].strip() if img_tag else ""
            imagem = img_tag["src"] if img_tag else None

            # Texto visível do link
            texto_card = card.get_text(separator=" ", strip=True)

            # Pega ano, marca e modelo se possível
            ano_match = re.search(r"\b(19|20)\d{2}\b", alt)
            ano = ano_match.group(0) if ano_match else None

            partes = alt.split()
            marca = partes[1].upper() if len(partes) > 1 else None
            modelo = " ".join(partes[2:]).split("no grupo")[0].strip().title()

            # Localização (tentativa)
            localizacao_match = re.search(r"no grupo (.*)$", alt)
            localizacao = localizacao_match.group(1).strip() if localizacao_match else None

            # Preço
            preco_match = re.search(r"R\$ ?[\d\.,]+", texto_card)
            preco = preco_match.group(0) if preco_match else None

            # Quilometragem - busca em todos os spans dentro do card
            spans = card.find_all("span")
            km = None
            for span in spans:
                texto_span = span.get_text(strip=True)
                if re.search(r"km", texto_span, re.IGNORECASE):
                    km_match = re.search(r"[\d\.,]+(?:\s?|&nbsp;)?mil|\d{4,6} ?km", texto_span.lower())
                    if km_match:
                        km = km_match.group(0).replace("&nbsp;", " ").strip()
                        break

            carros.append({
                "ano": ano,
                "marca": marca,
                "modelo": modelo,
                "localizacao": localizacao,
                "preco": preco,
                "km": km,
                "imagem": imagem,
                "descricao": alt,
                "link": link,
                "site_icon": "https://www.facebook.com/favicon.ico"
            })

        except Exception as e:
            print(f"[ERRO] {e}")
            continue

    return carros
