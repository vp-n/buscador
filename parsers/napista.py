import re
import json
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def identificar_favicon(link):
    dominio = urlparse(link).hostname or "napista.com.br"
    return f"https://www.google.com/s2/favicons?domain={dominio}&sz=64"

def extrair_carros_completos_napista(html):
    soup = BeautifulSoup(html, "html.parser")
    script_tag = soup.find("script", type="application/ld+json")
    localizacoes = soup.select("span.styles_listingCardLocation__MWNa8")

    if not script_tag:
        return []

    try:
        raw_data = json.loads(script_tag.string)
        if isinstance(raw_data, dict):
            raw_data = [raw_data]

        vehicles_data = next(
            (item.get("mainEntity", {}).get("itemListElement", [])
             for item in raw_data if item.get("@type") == "SearchResultsPage"),
            []
        )

        carros = []

        for idx, veiculo in enumerate(vehicles_data):
            try:
                oferta = veiculo.get("offers", [{}])[0]
                preco = int(oferta.get("priceSpecification", {}).get("price", 0))

                km_str = veiculo.get("mileageFromOdometer", "0 KM")
                km = int(re.sub(r"[^\d]", "", km_str))

                localizacao = localizacoes[idx].text.strip() if idx < len(localizacoes) else None

                descricao = veiculo.get("name", "")

                combustivel_match = re.search(r"(Flex|Gasolina|Diesel|Etanol|Elétrico)", descricao, re.IGNORECASE)
                combustivel = combustivel_match.group(1).capitalize() if combustivel_match else None

                cambio_match = re.search(r"(Automático|Manual)", descricao, re.IGNORECASE)
                cambio = cambio_match.group(1).capitalize() if cambio_match else None

                # Ano final (fabricação/modelo)
                ano_fabricacao = veiculo.get("productionDate", None)
                ano_modelo = veiculo.get("modelDate", None)
                ano = f"{ano_fabricacao}/{ano_modelo}" if ano_fabricacao and ano_modelo else None

                marca = veiculo.get("manufacturer", {}).get("name", "").strip()
                modelo = veiculo.get("model", "").strip()
                config = veiculo.get("vehicleConfiguration", "").strip()
                modelo_completo = f"{modelo} {config}".strip()

                carros.append({
                    "marca": marca or None,
                    "modelo": modelo_completo or None,
                    "preco": preco,
                    "localizacao": localizacao,
                    "quilometragem": km,
                    "combustivel": combustivel,
                    "ano": ano,
                    "cambio": cambio,
                    "imagem": veiculo.get("image", None),
                    "descricao": descricao,
                    "link": veiculo.get("@id", None),
                    "site_icon": identificar_favicon(veiculo.get("@id", "https://napista.com.br"))
                })

            except Exception:
                continue

        return carros

    except json.JSONDecodeError:
        return []