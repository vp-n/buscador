from flask import Flask, request, jsonify
import importlib

app = Flask(__name__)

@app.route('/get-dom', methods=['GET'])
def handle_dom():
    site = request.args.get('site')
    estado = request.args.get('estado')
    carro = request.args.get('carro')

    if not site or not estado or not carro:
        return jsonify({"error": "Parâmetros 'site', 'estado' e 'carro' são obrigatórios."}), 400

    try:
        # Tenta importar o módulo correspondente ao site
        module = importlib.import_module(f'crawlers.{site.lower()}')
        # Chama a função get_dom dentro do módulo
        dom = module.get_dom(estado, carro)
        return jsonify({"dom": dom})
    except ModuleNotFoundError:
        return jsonify({"error": f"Crawler para '{site}' não encontrado."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
