from flask import Flask, request, jsonify
from fake_useragent import UserAgent
from playwright.sync_api import sync_playwright

ua = UserAgent()
app = Flask(__name__)

@app.route('/get-dom', methods=['GET'])
def get_dom():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "Parâmetro 'url' é obrigatório."}), 400

    try:
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

            # Técnicas stealth JS (remove webdriver flag, etc.)
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

            # Acessa a URL
            page.goto(url, timeout=360000)
            page.wait_for_load_state("networkidle", timeout=360000)

            dom = page.content()
            browser.close()

        return jsonify({"dom": dom})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
