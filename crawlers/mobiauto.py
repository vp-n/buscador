# crawlers/mobiauto.py
from fake_useragent import UserAgent
from playwright.sync_api import sync_playwright
import time

ua = UserAgent()

estado_cidade_nome = {
    "mg": "belo horizonte",
    "pa": "belem",
    "rr": "boa vista",
    "df": "brasilia",
    "ms": "campo grande",
    "mt": "cuiaba",
    "pr": "curitiba",
    "sc": "florianopolis",
    "ce": "fortaleza",
    "go": "goiania",
    "pb": "joao pessoa",
    "ap": "macapa",
    "al": "maceio",
    "am": "manaus",
    "rn": "natal",
    "to": "palmas",
    "rs": "porto alegre",
    "ro": "porto velho",
    "pe": "recife",
    "ac": "rio branco",
    "rj": "rio de janeiro",
    "ba": "salvador",
    "ma": "sao luis",
    "sp": "sao paulo",
    "pi": "teresina",
    "es": "vitoria"
}

def monta_url_mobiauto(estado, marca, modelo):
    cidade = estado_cidade_nome.get(estado.lower())
    if not cidade:
        raise ValueError(f"Estado '{estado}' não mapeado.")

    estado_slug = estado.lower()
    cidade_slug = cidade.lower().replace(" ", "-")
    marca_slug = marca.lower().replace(" ", "-")
    modelo_slug = modelo.lower().replace(" ", "-")

    return f"https://www.mobiauto.com.br/comprar/carros/{estado_slug}-{cidade_slug}/{marca_slug}/{modelo_slug}"

def get_dom(estado, marca, modelo):
    url = monta_url_mobiauto(estado, marca, modelo)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent=ua.random,
            locale="pt-BR",
            timezone_id="America/Sao_Paulo",
            viewport={"width": 1366, "height": 768},
            ignore_https_errors=True,
            java_script_enabled=True,
        )
        page = context.new_page()

        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            window.chrome = { runtime: {} };
            Object.defineProperty(navigator, 'languages', { get: () => ['pt-BR', 'pt'] });
            Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3] });
        """)

        page.goto(url, timeout=60000)
        page.wait_for_load_state("networkidle", timeout=60000)

        # 👉 Desce a página um pouco para carregar mais elementos
        page.mouse.wheel(0, 1000)
        time.sleep(2)

        page.mouse.wheel(0, 1000)
        time.sleep(2)

        page.mouse.wheel(0, 1000)
        time.sleep(2)





        dom = page.content()
        browser.close()
        return dom
