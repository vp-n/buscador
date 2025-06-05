from flask import Flask, request, jsonify
import importlib

app = Flask(__name__)

@app.route('/get-dom', methods=['GET'])
def handle_dom():
    site = request.args.get('site')
    estado = request.args.get('estado')
    carro = request.args.get('carro')
    modelo = request.args.get('modelo')

    if not site or not estado or not carro:
        return jsonify({"error": "Parâmetros 'site', 'estado' e 'carro' são obrigatórios."}), 400

    try:
        # 1. Importa dinamicamente o módulo do crawler (ex: crawlers.olx)
        crawler_module = importlib.import_module(f'crawlers.{site.lower()}')
        dom = crawler_module.get_dom(estado, carro, modelo)

        # 2. Importa dinamicamente o módulo do parser (ex: parsers.olx)
        parser_module = importlib.import_module(f'parsers.{site.lower()}')
        extrair_func = getattr(parser_module, f"extrair_carros_completos_{site.lower()}")

        # 3. Extrai os dados do HTML
        carros = extrair_func(dom)
        #return jsonify({"dom": dom, "carros": carros})
        return jsonify(carros)
        #return jsonify(dom)

    except ModuleNotFoundError:
        return jsonify({"error": f"Site '{site}' não suportado (crawler ou parser não encontrado)."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)