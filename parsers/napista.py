import re
import json
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def identificar_favicon(link):
    dominio = urlparse(link).hostname or ""
    return f"https://www.google.com/s2/favicons?domain={dominio}&sz=64"

def extrair_carros_completos_napista(html):
    soup = BeautifulSoup(html, "html.parser")
    script_tag = soup.find("script", type="application/ld+json")
    localizacoes = soup.select("span.styles_listingCardLocation__MWNa8")

    if not script_tag:
        return []

    try:
        data = json.loads(script_tag.string)
        vehicles_data = next(
            (item["mainEntity"]["itemListElement"]
             for item in data if item.get("@type") == "SearchResultsPage"),
            []
        )

        carros = []

        for idx, veiculo in enumerate(vehicles_data):
            try:
                preco = int(veiculo.get("offers", [{}])[0]
                            .get("priceSpecification", {}).get("price", 0))
                km_str = veiculo.get("mileageFromOdometer", "0 KMT")
                km = int(re.sub(r"[^\d]", "", km_str))

                # Localização do card (pegando pelo índice correspondente)
                localizacao = localizacoes[idx].text.strip() if idx < len(localizacoes) else None

                # Tentativa de inferir combustível
                descricao = veiculo.get("name", "")
                combustivel_match = re.search(r"(Flex|Gasolina|Diesel|Etanol|Elétrico)", descricao, re.IGNORECASE)
                combustivel = combustivel_match.group(1).capitalize() if combustivel_match else None

                carros.append({
                    "marca": veiculo.get("manufacturer", {}).get("name"),
                    "modelo": f"{veiculo.get('model')} {veiculo.get('vehicleConfiguration')}",
                    "preco": preco,
                    "localizacao": localizacao,
                    "quilometragem": km,
                    "combustivel": combustivel,
                    "imagem": veiculo.get("image"),
                    "descricao": descricao,
                    "link": veiculo.get("@id"),
                    "site_icon": identificar_favicon(veiculo.get("@id", "https://napista.com.br"))
                })
            except Exception:
                continue

        return carros

    except json.JSONDecodeError:
        return []