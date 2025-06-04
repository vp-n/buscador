from fake_useragent import UserAgent
from playwright.sync_api import sync_playwright

ua = UserAgent()

#def get_dom(estado, carro):
def get_dom(carro):
    # Substitui espaço por hífen e coloca em minúsculo (formato usado na URL)
    carro_formatado = carro.lower().replace(" ", "-")
    url = f"https://www.napista.com.br/busca/{carro_formatado}?pn=1"

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

        # Stealth simples
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

        page.goto(url, timeout=120000)
        page.wait_for_load_state("networkidle", timeout=120000)

        dom = page.content()
        browser.close()

    return dom
