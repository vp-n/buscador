import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def identificar_favicon(link):
    dominio = urlparse(link).hostname or "www.mobiauto.com.br"
    return f"https://www.google.com/s2/favicons?domain={dominio}&sz=64"


def extrair_carros_completos_mobiauto(html):
    soup = BeautifulSoup(html, "html.parser")
    cards = soup.select("div.deal-card")
    carros = []

    for card in cards:
        try:
            # Link
            a_tag = card.find("a", href=True)
            link = a_tag["href"] if a_tag else None
            if link and not link.startswith("http"):
                link = f"https://www.mobiauto.com.br{link}"
            if not link:
                continue

            # Pega marca, modelo, ano e versão da URL
            marca = modelo = versao_url = ano = cambio = None
            try:
                partes = link.split("/comprar/carros/")[1].split("/")
                if len(partes) >= 6:
                    marca = partes[1].upper()               # ex: CHEVROLET
                    modelo_base = partes[2].upper()         # ex: ONIX
                    ano = partes[3]                         # ex: 2023
                    versao_url = partes[4].replace("-", " ").title()  # ex: Lt 1 0 Turbo Aut
                    modelo = f"{modelo_base} {versao_url}".strip()    # Modelo completo
            except Exception:
                pass

            # Descrição (nome e versão do carro)
            descricao_tag = card.select_one("div.css-1qtpr08 a h2.css-1exrr02")
            descricao_final = card.select_one("div.css-1qtpr08 a h3.css-8p76iz")
            marca_modelo = descricao_tag.text.strip() if descricao_tag else ""
            versao_texto = descricao_final.text.strip() if descricao_final else ""
            descricao = f"{marca_modelo} {versao_texto}".strip()

            # Câmbio (entre parênteses)
            cambio_match = re.search(r"\(([^)]+)\)", versao_texto)
            cambio = cambio_match.group(1).replace(".", "").strip() if cambio_match else None

            # Localização
            local_tag = card.select_one("div.css-1qtpr08 a div.css-1e8ic5x div.css-m3w4si p.css-1907xyf")
            localizacao = local_tag.text.strip() if local_tag else None

            # Quilometragem
            km_tag = card.select_one("div.css-1qtpr08 a div.css-1e8ic5x p.css-1907xyf")
            km = None
            if km_tag:
                texto = km_tag.text.strip().lower().replace("km", "").replace(".", "").strip()
                try:
                    km = int(texto)
                except ValueError:
                    pass

            # Preço
            preco_tag = card.select_one("div.css-1qtpr08 div.css-8bcs29 div.css-452kem p.css-1u3gc91")
            preco = None
            if preco_tag:
                texto = preco_tag.text.strip().replace("R$", "").replace(".", "").replace(",", ".")
                try:
                    preco = float(texto)
                except ValueError:
                    pass

            # Combustível
            combustivel_match = re.search(r"(Flex|Gasolina|Diesel|Etanol|Elétrico)", descricao, re.IGNORECASE)
            combustivel = combustivel_match.group(1).capitalize() if combustivel_match else None

            # Imagem
            imagem = None
            img_tag = card.find("img", class_="deal-next-image-desktop")
            if img_tag and img_tag.get("src"):
                imagem = img_tag["src"].strip()
            if not imagem:
                for img in card.find_all("img"):
                    src = img.get("src", "") or ""
                    srcset = img.get("srcset", "")
                    if "mobiauto.com.br" in src:
                        imagem = src.strip()
                        break
                    elif "mobiauto.com.br" in srcset:
                        imagem = srcset.split(",")[-1].split()[0].strip()
                        break

            # Adiciona ao resultado
            carros.append({
                "marca": marca,
                "modelo": modelo,
                "ano": ano,
                "cambio": cambio,
                "descricao": descricao,
                "preco": preco,
                "quilometragem": km,
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