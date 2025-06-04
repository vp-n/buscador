from flask import Flask, request, jsonify
import importlib

app = Flask(__name__)

@app.route('/get-dom', methods=['GET'])
def handle_dom():
    site = request.args.get('site')
    estado = request.args.get('estado')
    carro = request.args.get('carro')  # Pode ser "modelo" ou "carro"
    marca = request.args.get('marca')  # Nova variável para marca

    # Validação dos parâmetros básicos
    if not site or not estado or not carro:
        return jsonify({"error": "Parâmetros 'site', 'estado' e 'carro' são obrigatórios."}), 400

    try:
        # Importa o módulo do crawler conforme o site informado
        module = importlib.import_module(f'crawlers.{site.lower()}')

        if site.lower() == "webmotors":
            # Webmotors precisa de marca também
            if not marca:
                return jsonify({"error": "Parâmetro 'marca' é obrigatório para o site Webmotors."}), 400
            # Chama get_dom com estado, marca e carro
            dom = module.get_dom(estado, marca, carro)
        else:
            # Para outros sites, só estado e carro são necessários
            dom = module.get_dom(estado, carro)

        return jsonify({"dom": dom})

    except ModuleNotFoundError:
        return jsonify({"error": f"Crawler para '{site}' não encontrado."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)