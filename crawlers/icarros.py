# em crawlers/icarros.py

from fake_useragent import UserAgent
from playwright.sync_api import sync_playwright

ua = UserAgent()

# Dicionário com alguns estados e seus códigos iCarros (exemplos)
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


def monta_url_icarros(estado, carro):
    cidade = estado_cidade_nome.get(estado.lower())
    if not cidade:
        raise ValueError(f"Estado '{estado}' não mapeado no dicionário.")

    cidade_slug = cidade.lower().replace(" ", "-")
    estado_slug = estado.lower()
    carro_slug = carro.lower().replace(" ", "-")

    return f"https://www.icarros.com.br/comprar/{cidade_slug}-{estado_slug}/{carro_slug}/"

def get_dom(estado, carro):
    url = monta_url_icarros(estado, carro)

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

        # Stealth
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            });
            window.chrome = { runtime: {}, loadTimes: () => {}, csi: () => {} };
            Object.defineProperty(navigator, 'languages', { get: () => ['pt-BR', 'pt'] });
            Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3] });
        """)

        tentativas = 2
        for tentativa in range(tentativas):
            try:
                print(f"Tentativa {tentativa + 1} de {tentativas} para acessar: {url}")
                page.goto(url, timeout=60000)
                page.wait_for_load_state("networkidle", timeout=60000)
                dom = page.content()

                # Se o DOM for muito pequeno, tenta novamente (página possivelmente falhou)
                if len(dom) < 5000 and tentativa < tentativas - 1:
                    print("DOM muito pequeno, recarregando página...")
                    page.reload()
                    continue

                # Limpa linhas vazias
                dom_limpado = "\n".join([linha for linha in dom.splitlines() if linha.strip() != ""])
                return dom_limpado

            except Exception as e:
                print("Erro ao tentar carregar a página:", e)
                if tentativa < tentativas - 1:
                    print("Tentando novamente...")
                    page.reload()
                else:
                    raise e
        browser.close()

    return dom_limpado

