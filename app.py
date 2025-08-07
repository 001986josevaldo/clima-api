# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from ClimaController import ClimaController

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/clima')
def clima_por_cep():
    cep = request.args.get('cep')
    print("CEP recebido:", cep)

    if not cep:
        return jsonify({
            "erro": "CEP não informado",
            "exemplo": "/clima?cep=01001000"
        }), 400

    return jsonify({
        "mensagem": "CEP recebido com sucesso",
        "cep": cep
    })

    cep = cep.replace("-", "").strip()

    try:
        controller = ClimaController()
        resultado = controller.buscar(cep)
        return jsonify(resultado)

    except Exception as e:
        print("Erro inesperado:", str(e))
        return jsonify({"erro": "Erro no processamento", "detalhes": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
