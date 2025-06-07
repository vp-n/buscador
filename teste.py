from flask import Flask, request, jsonify
import importlib

app = Flask(__name__)

@app.route('/get-dom', methods=['GET'])
def handle_dom():
    site = request.args.get('site')
    estado = request.args.get('estado')
    carro = request.args.get('carro')
    marca = request.args.get('marca')
    modelo = request.args.get('modelo')  # novo parâmetro

    if not site:
        return jsonify({"error": "Parâmetro 'site' é obrigatório."}), 400

    # Validação por site
    if site.lower() == "napista":
        if not carro:
            return jsonify({"error": "Parâmetro 'carro' é obrigatório para o site Napista."}), 400

    elif site.lower() == "webmotors":
        # agora requer estado, marca e modelo
        if not estado or not marca or not modelo:
            return jsonify({"error": "Parâmetros 'estado', 'marca' e 'modelo' são obrigatórios para o site WebMotors."}), 400

    elif site.lower() == "mobiauto":
        if not estado or not marca or not carro:
            return jsonify({"error": f"Parâmetros 'estado', 'marca' e 'carro' são obrigatórios para o site {site.title()}."}), 400

    else:
        if not estado or not carro:
            return jsonify({"error": f"Parâmetros 'estado' e 'carro' são obrigatórios para o site {site.title()}."}), 400

    try:
        # Importa crawler dinamicamente
        crawler_module = importlib.import_module(f'crawlers.{site.lower()}')

        # Chama get_dom conforme o site
        if site.lower() == "napista":
            dom = crawler_module.get_dom(carro)
        elif site.lower() == "webmotors":
            dom = crawler_module.get_dom(estado, marca, modelo)  # <-- alterado aqui
        elif site.lower() == "mobiauto":
            dom = crawler_module.get_dom(estado, carro, marca)
        else:
            dom = crawler_module.get_dom(estado, carro)

        # Importa parser dinamicamente
        parser_module = importlib.import_module(f'parsers.{site.lower()}')
        extrair_func = getattr(parser_module, f"extrair_carros_completos_{site.lower()}")

        # Extrai dados do HTML
        carros = extrair_func(dom)
        return jsonify(carros)

    except ModuleNotFoundError:
        return jsonify({"error": f"Crawler ou parser para '{site}' não encontrado."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
