from fake_useragent import UserAgent
from playwright.sync_api import sync_playwright
import time

ua = UserAgent()

def get_dom(estado, carro):
    url = f"https://www.olx.com.br/estado-{estado}?q={carro}"

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

        print(f"Acessando: {url}")
        page.goto(url, timeout=60000)

        # Espera a página carregar visualmente
        time.sleep(3)

        # Dá F5 (reload) e espera mais 10 segundos
        print("F5 #1...")
        page.reload()
        time.sleep(2)

        dom = page.content()

        dom = page.content()
        browser.close()

    return dom
