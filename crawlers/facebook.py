from fake_useragent import UserAgent
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

ua = UserAgent()

estado_cidade_slug = {
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

def monta_url_facebook(estado, carro):
    cidade_slug = estado_cidade_slug.get(estado.lower())
    if not cidade_slug:
        raise ValueError(f"Estado '{estado}' não mapeado.")
    carro_slug = carro.lower().replace(" ", "+")
    return f"https://www.facebook.com/marketplace/{cidade_slug}/search/?query={carro_slug}"

def get_dom(estado, carro):
    url = monta_url_facebook(estado, carro)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Use True se quiser rodar em background
        context = browser.new_context(
            user_agent=ua.random,
            locale="pt-BR",
            timezone_id="America/Sao_Paulo",
            viewport={"width": 1366, "height": 768},
            ignore_https_errors=True,
            java_script_enabled=True,
        )
        page = context.new_page()

        # Stealth para parecer humano
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            window.chrome = {runtime: {}};
            Object.defineProperty(navigator, 'languages', {get: () => ['pt-BR', 'pt']});
            Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3]});
        """)

        page.goto(url, timeout=70000)
        page.wait_for_load_state("domcontentloaded")

        # Tenta fechar o modal de login se aparecer
        try:
            close_button = page.wait_for_selector('div[aria-label="Fechar"]', timeout=5000)
            close_button.click()
            page.wait_for_timeout(3000)
        except PlaywrightTimeoutError:
            print("Modal de login não apareceu.")

        # Rola a página para carregar os anúncios
        page.mouse.wheel(0, 3000)
        page.wait_for_timeout(5000)

        dom = page.content()
        browser.close()
        return dom
