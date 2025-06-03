from fake_useragent import UserAgent
from playwright.sync_api import sync_playwright
import urllib.parse

ua = UserAgent()

estado_cidade_coords = {
    "mg": ("belo horizonte", "-19.920830,-43.937778"),
    "pa": ("belem", "-1.455833,-48.502222"),
    "rr": ("boa vista", "2.819444,-60.673611"),
    "df": ("brasilia", "-15.793889,-47.882778"),
    "ms": ("campo grande", "-20.442778,-54.646944"),
    "mt": ("cuiaba", "-15.601389,-56.097778"),
    "pr": ("curitiba", "-25.428333,-49.273056"),
    "sc": ("florianopolis", "-27.594444,-48.548611"),
    "ce": ("fortaleza", "-3.717222,-38.543056"),
    "go": ("goiania", "-16.686389,-49.264444"),
    "pb": ("joao pessoa", "-7.115,-34.863056"),
    "ap": ("macapa", "0.038889,-51.066389"),
    "al": ("maceio", "-9.665833,-35.735"),
    "am": ("manaus", "-3.1190275,-60.0217314"),
    "rn": ("natal", "-5.795,-35.211111"),
    "to": ("palmas", "-10.244167,-48.355833"),
    "rs": ("porto alegre", "-30.027778,-51.228056"),
    "ro": ("porto velho", "-8.760278,-63.900833"),
    "pe": ("recife", "-8.05428,-34.8813"),
    "ac": ("rio branco", "-9.97472,-67.81"),
    "rj": ("rio de janeiro", "-22.9068,-43.1729"),
    "ba": ("salvador", "-12.9714,-38.5014"),
    "ma": ("sao luis", "-2.53874,-44.2821"),
    "sp": ("sao paulo", "-23.55052,-46.633308"),
    "pi": ("teresina", "-5.08921,-42.8016"),
    "es": ("vitoria", "-20.3155,-40.3128")
}

def monta_url_webmotors(estado, marca, modelo, pagina=1):
    info = estado_cidade_coords.get(estado.lower())
    if not info:
        raise ValueError(f"Estado '{estado}' não mapeado no dicionário.")

    cidade, coords = info

    estado_slug = estado.lower()
    cidade_slug = cidade.lower().replace(" ", "-")
    marca_slug = marca.lower()
    modelo_slug = modelo.lower()

    base_url = f"https://www.webmotors.com.br/carros/{estado_slug}-{cidade_slug}/{marca_slug}/{modelo_slug}"

    query_params = {
        "lkid": "1948",
        "tipoveiculo": "carros",
        "localizacao": f"{coords}x100km",
        "estadocidade": f"{cidade.capitalize()}-{cidade_slug}",
        "marca1": modelo.upper(),
        "modelo1": marca.upper(),
        "page": str(pagina)
    }

    query_string = urllib.parse.urlencode(query_params, safe='')
    return f"{base_url}?{query_string}"

def get_dom(estado, carro, marca):
    url = monta_url_webmotors(estado, marca, carro)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        context = browser.new_context(
            user_agent=ua.random,
            locale="pt-BR",
            timezone_id="America/Sao_Paulo",
            viewport={"width": 1366, "height": 768},
            ignore_https_errors=True,
            java_script_enabled=True,
        )

        page = context.new_page()

        # Stealth para não parecer automação
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            });

            window.chrome = {
                runtime: {},
                loadTimes: function() {},
                csi: function() {},
            };

            Object.defineProperty(navigator, 'languages', {
                get: () => ['pt-BR', 'pt']
            });

            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3]
            });
        """)

        page.goto(url, timeout=60000)
        page.wait_for_load_state("networkidle", timeout=60000)

        dom = page.content()
        browser.close()

    return dom
