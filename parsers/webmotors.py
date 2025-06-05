from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re

def identificar_favicon(link):
    dominio = urlparse(link).hostname or "www.webmotors.com.br"
    return f"https://www.google.com/s2/favicons?domain={dominio}&sz=64"

def extrair_carros_completos_webmotors(html):
    soup = BeautifulSoup(html, "html.parser")
    cards = soup.select("div._Card_18bss_1")

    carros = []
    links_vistos = set()

    for card in cards:
        try:
            # Link do anúncio
            a_tag = card.select_one("a[href]")
            link = a_tag["href"] if a_tag else None
            if link and not link.startswith("http"):
                link = f"https://www.webmotors.com.br{link}"
            if not link or link in links_vistos:
                continue
            links_vistos.add(link)

            # Descrição e imagem
            img_tag = card.select_one("img")
            descricao = img_tag["alt"].strip() if img_tag and img_tag.get("alt") else None
            imagem = img_tag["src"] if img_tag and img_tag.get("src") else None

            # Marca e modelo
            marca = modelo = None
            if descricao:
                partes = descricao.split()
                if len(partes) >= 2:
                    marca = partes[0].upper()
                    modelo = partes[1].upper()

            # Ano e câmbio pela URL
            cambio = None
            try:
                partes = link.split("/comprar/")[1].split("/")
                if len(partes) >= 6:
                    versao_url = partes[2].replace("-", " ").upper()
                    cambio_match = re.search(r"(AUT|MANUAL)", versao_url)
                    cambio = cambio_match.group(1).capitalize() if cambio_match else None
            except Exception:
                pass

            # Preço
            preco = None
            preco_tag = card.select_one("p._web-subtitle-medium_qtpsh_69")
            if not preco_tag:
                preco_tag = card.find(text=re.compile(r"R\$"))
                if preco_tag:
                    preco_tag = preco_tag.parent
            if preco_tag:
                preco_texto = preco_tag.get_text(strip=True)
                preco_match = re.search(r"\d[\d\.\,]*", preco_texto)
                if preco_match:
                    preco = float(preco_match.group().replace(".", "").replace(",", "."))

            # Ano e quilometragem
            ano = quilometragem = None
            infos = card.select("p._body-regular-small_qtpsh_152")
            if len(infos) >= 2:
                ano = infos[0].get_text(strip=True)
                km_texto = infos[1].get_text(strip=True)
                km_match = re.search(r"[\d\.]+", km_texto)
                if km_match:
                    quilometragem = int(km_match.group().replace(".", ""))

            # Combustível
            combustivel = None
            if descricao:
                combustiveis = ["Flex", "Gasolina", "Diesel", "Elétrico", "Híbrido"]
                for tipo in combustiveis:
                    if tipo.upper() in descricao.upper():
                        combustivel = tipo
                        break

            # Localização segura (pegar só se houver uma terceira info)
            localizacao = None
            if len(infos) >= 3:
                localizacao = infos[2].get_text(strip=True)

            carros.append({
                "marca": marca,
                "modelo": modelo,
                "ano": ano,
                "cambio": cambio,
                "descricao": descricao,
                "preco": preco,
                "quilometragem": quilometragem,
                "combustivel": combustivel,
                "localizacao": localizacao,
                "imagem": imagem,
                "link": link,
                "site_icon": identificar_favicon(link)
            })

        except Exception as e:
            print(f"[ERRO] Falha ao processar card: {e}")
            continue

    return carros
