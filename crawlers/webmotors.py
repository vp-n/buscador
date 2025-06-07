import urllib.parse
import requests

def gerar_url_webmotors(marca, modelo, estado, sigla_estado, page=1):
    marca_lower = marca.lower()
    modelo_lower = modelo.lower()
    marca_upper = marca.upper()
    modelo_upper = modelo.upper()

    base_url = "https://www.webmotors.com.br/carros"

    url_param = (
        f"{base_url}/{sigla_estado}/{marca_lower}/{modelo_lower}"
        f"?autocomplete={modelo_lower}"
        f"&autocompleteTerm={marca_upper}%20{modelo_upper}"
        f"&lkid=1705"
        f"&tipoveiculo=carros"
        f"&estadocidade={estado}"
        f"&marca1={marca_upper}"
        f"&modelo1={modelo_upper}"
        f"&page={page}"
    )

    return url_param


def get_dom(estado, marca, modelo, page=1):
    sigla_estado = estado.lower()[:2]
    url = gerar_url_webmotors(marca, modelo, estado, sigla_estado, page)

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "text/html",
        "Referer": "https://www.webmotors.com.br/"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text  # Retorna HTML bruto
    except requests.exceptions.RequestException as e:
        return f"ERRO: {e}"
