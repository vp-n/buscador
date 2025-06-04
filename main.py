from flask import Flask, request, jsonify
import importlib

app = Flask(__name__)

@app.route('/get-dom', methods=['GET'])
def handle_dom():
    site = request.args.get('site')
    estado = request.args.get('estado')
    carro = request.args.get('carro')  # Modelo ou nome do carro
    marca = request.args.get('marca')  # Só necessário para alguns sites

    if not site or not carro or (site.lower() != "napista" and not estado):
        return jsonify({"error": "Parâmetros 'site', 'estado' e 'carro' são obrigatórios (exceto 'estado' para o site napista)."}), 400

    try:
        module = importlib.import_module(f'crawlers.{site.lower()}')

        if site.lower() in ["webmotors", "mobiauto"]:
            if not marca:
                return jsonify({"error": f"Parâmetro 'marca' é obrigatório para o site {site}."}), 400
            dom = module.get_dom(estado, marca, carro)

        elif site.lower() == "napista":
            dom = module.get_dom(carro)

        else:
            dom = module.get_dom(estado, carro)

        return jsonify({"dom": dom})

    except ModuleNotFoundError:
        return jsonify({"error": f"Crawler para '{site}' não encontrado."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)