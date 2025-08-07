# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from ClimaController import ClimaController
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return jsonify({
        "mensagem": "✅ API Clima ativa!",
        "exemplo": "/clima?cep=01001000"
    })

@app.route('/clima')
def clima_por_cep():
    cep = request.args.get('cep')
    print("CEP recebido:", cep)

    if not cep:
        return jsonify({
            "erro": "CEP não informado",
            "exemplo": "/clima?cep=01001000"
        }), 400

    cep = cep.replace("-", "").strip()

    try:
        controller = ClimaController()
        resultado = controller.buscar(cep)
        return jsonify(resultado)

    except Exception as e:
        print("Erro inesperado:", str(e))
        return jsonify({
            "erro": "Erro no processamento",
            "detalhes": str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Necessário para Railway
    app.run(host='0.0.0.0', port=port, debug=True)
