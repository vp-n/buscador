from bs4 import BeautifulSoup
import re

def extrair_carros_completos_facebook(html):
    soup = BeautifulSoup(html, "html.parser")
    cards = soup.select("a[href^='/marketplace/item/']")

    carros = []

    for card in cards:
        try:
            href = card.get("href", "")
            link = "https://www.facebook.com" + href

            img_tag = card.find("img", alt=True)
            alt = img_tag["alt"].strip() if img_tag else ""
            imagem = img_tag["src"] if img_tag else None

            if not re.search(r"\d{4}.*(FIAT|CHEVROLET|FORD|TOYOTA|HONDA|VOLKSWAGEN|RENAULT)", alt, re.IGNORECASE):
                continue

            # Ano
            ano_match = re.match(r"(\d{4})", alt)
            ano = ano_match.group(1) if ano_match else None

            # Marca e modelo
            partes = alt.split()
            marca = partes[1].upper() if len(partes) > 1 else None
            modelo = " ".join(partes[2:]).split("no grupo")[0].strip().title()

            # Local
            localizacao_match = re.search(r"no grupo (.*)$", alt)
            localizacao = localizacao_match.group(1).strip() if localizacao_match else None

            carros.append({
                "ano": ano,
                "marca": marca,
                "modelo": modelo,
                "localizacao": localizacao,
                "imagem": imagem,
                "descricao": alt,
                "link": link,
                "site_icon": "https://www.facebook.com/favicon.ico"
            })

        except Exception as e:
            print(f"[ERRO] {e}")
            continue

    return carros