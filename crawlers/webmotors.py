import urllib.parse
import requests

def gerar_url_api_webmotors(marca, modelo, estado, sigla_estado, page=1):
    marca_upper = marca.upper()
    modelo_upper = modelo.upper()
    marca_lower = marca.lower()
    modelo_lower = modelo.lower()

    url_param = (
        f"https://www.webmotors.com.br/carros/{sigla_estado}/{marca_lower}/{modelo_lower}"
        f"?autocomplete={modelo_lower}"
        f"&autocompleteTerm={marca_upper}%20{modelo_upper}"
        f"&lkid=1705"
        f"&tipoveiculo=carros"
        f"&estadocidade={estado}"
        f"&marca1={marca_upper}"
        f"&modelo1={modelo_upper}"
        f"&page={page}"
    )

    query_params = {
        "displayPerPage": "47",
        "actualPage": str(page),
        "showMenu": "true",
        "showCount": "true",
        "showBreadCrumb": "true",
        "order": "1",
        "url": urllib.parse.quote(url_param, safe=""),
        "mediaZeroKm": "true",
        "channel": "36"
    }

    base_url = "https://www.webmotors.com.br/api/search/car"
    query_string = "&".join([f"{k}={v}" for k, v in query_params.items()])
    return f"{base_url}?{query_string}"

def get_dom(estado, marca, modelo, page=1):
    sigla_estado = estado.lower()[:2]
    url = gerar_url_api_webmotors(marca, modelo, estado, sigla_estado, page)

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Referer": "https://www.webmotors.com.br/"
    }

    print(f"[INFO] URL final chamada: {url}")  # 👈 Mostra a URL para debug

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        json_data = response.json()
        print(f"[INFO] Resultados encontrados: {len(json_data.get('SearchResults', []))}")
        return {"dom": json_data}  # 👈 Importante: retornar com chave 'dom' para o parser funcionar!
    except requests.exceptions.RequestException as e:
        print(f"[ERRO] Falha na requisição: {e}")
        return {"error": str(e)}
